import sqlite3

from config_local import bot

# Creating database
connection = sqlite3.connect('wishlists.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS wishlists (chat_id INTEGER, topic TEXT, item TEXT, item_number INTEGER)")
connection.commit()


# Handling with /start command
@bot.message_handler(commands=['start'])
def start_message(message):
    # Greeting of user
    greeting = f'Hello, {message.from_user.first_name}!'
    bot.send_message(message.chat.id, greeting)

    # List of commands
    bot.send_message(message.chat.id, 'What you want to do?\n\n'
                                      '/new_wishlist - creating a new wishlist\n'
                                      '/open_wishlist - open and show your existing wishlist\n'
                                      '/add - add items to your wishlist\n'
                                      '/delete - delete items from your wishlist\n'
                                      '/commands - to see a list of commands for operating with wishlists')


# Handling with /add command
@bot.message_handler(commands=['add'])
def add_command(message):
    bot.send_message(message.chat.id, 'Write wishlist name:')
    message_for_user = 'Write item which you want to add to chosen topic:'
    operation = 'add'
    bot.register_next_step_handler(message, get_topic_name, message_for_user, operation)


# Handling with /delete command
@bot.message_handler(commands=['delete'])
def delete_command(message):
    bot.send_message(message.chat.id, 'Write wishlist name:')
    message_for_user = 'Write number of item which you want to delete from chosen topic:'
    operation = 'delete'
    bot.register_next_step_handler(message, get_topic_name, message_for_user, operation)


# Handling with /open_wishlist command
@bot.message_handler(commands=['open_wishlist'])
def open_wishlist_command(message):
    bot.send_message(message.chat.id, 'Write wishlist name:')
    operation = 'open_wishlist'
    message_for_user = 'One moment, please...'
    bot.register_next_step_handler(message, get_topic_name, message_for_user, operation)


# Handling with /new_wishlist command
@bot.message_handler(commands=['new_wishlist'])
def new_wishlist_command(message):
    bot.send_message(message.chat.id, 'Write name of your wishlist which you want to create:')
    message_for_user = 'Creating...'
    operation = 'new_wishlist'
    bot.register_next_step_handler(message, get_topic_name, message_for_user, operation)


# Handling with /commands
@bot.message_handler(commands=['commands'])
def commands_command(message):
    bot.send_message(message.chat.id, 'List of available commands:\n\n'
                                      '/new_wishlist - creating a new wishlist\n'
                                      '/open_wishlist - open and show your existing wishlist\n'
                                      '/add - add items to your wishlist\n'
                                      '/delete - delete items from your wishlist')


# Here we get topic name from user and use it for operating with database in further functions
def get_topic_name(message, message_for_user, operation):
    chat_id = message.chat.id
    topic = message.text
    bot.send_message(message.chat.id, message_for_user)

    if operation == 'new_wishlist':
        create_new_wishlist(message, topic)
    else:
        # Check for topic existence in db
        cursor.execute("SELECT * FROM wishlists WHERE chat_id = ? AND topic = ?", (chat_id, topic))
        items = cursor.fetchall()

        # If there is no such topic related to user - output message about it, else list all items in user's topic name
        if len(items) == 0:
            bot.send_message(message.chat.id, "Sorry, seems like you don't have such wishlist, please rewrite or "
                                              "create wishlist with chosen topic using /new_wishlist")
        else:
            # We get operation value from command handlers, so we know which function we should call
            if operation == 'add':
                bot.register_next_step_handler(message, add_item, topic)
            elif operation == 'open_wishlist':
                open_existing_wishlist(message, topic)
            else:
                bot.register_next_step_handler(message, delete_item, topic)


# Function for showing wishlist with chosen topic to user
def open_existing_wishlist(message, topic):
    # Selecting items from db by user chat id and topic name
    chat_id = message.chat.id
    cursor.execute("SELECT * FROM wishlists WHERE chat_id = ? AND topic = ?", (chat_id, topic))
    items = cursor.fetchall()

    # If there is no such topic related to user - output message about it, else list all items in user's topic name
    response = f"Topic: {topic}\n"
    for item in items:
        if item[2] is not None and item[3] is not None:
            response += f"{item[3]}. {item[2]}\n"

    bot.send_message(message.chat.id, response)
    bot.send_message(message.chat.id, "Use /commands to see all available commands")


# Function for creating a new wishlist with given topic and user chat id
def create_new_wishlist(message, topic):
    chat_id = message.chat.id
    cursor.execute("INSERT INTO wishlists VALUES (?, ?, NULL, NULL)", (chat_id, topic))
    connection.commit()
    bot.send_message(message.chat.id, 'Congratulations, your wishlist has been added! Now you can add items '
                                      'using this command: /add')


# Function for adding item to existing wishlist by given topic and user chat id
def add_item(message, topic):
    chat_id = message.chat.id
    item = message.text

    # There is some feature: numerating items, so user in future can easily delete them, without typing whole item name
    cursor.execute("SELECT * FROM wishlists WHERE `chat_id` = ? AND `topic` = ?", (chat_id, topic))
    item_number = len(cursor.fetchall())
    cursor.execute("INSERT INTO wishlists VALUES (?, ?, ?, ?)", (chat_id, topic, item, item_number))
    connection.commit()
    bot.send_message(message.chat.id,
                     "Success! Your item has been added. Use /open_wishlist to see all items in your wishlist")


# Function for deleting item from existing wishlist by given topic and user chat id
def delete_item(message, topic):
    chat_id = message.chat.id
    item_number = int(message.text)

    # Delete by item number in user's wishlist
    cursor.execute("DELETE FROM wishlists WHERE `chat_id` = ? AND `topic` = ? AND `item_number` = ?",
                   (chat_id, topic, item_number))
    connection.commit()

    # Changing all lower item numbers from deleted item by extracting one. Why: for example user deleted 4th item in
    # list, so 5th should replace it and get 4th item number, 6th to 5th, 7th to 6th and so on. We just get maximal item
    # number in list and decrease all item numbers from deleted item to this maximum - by one

    cursor.execute("SELECT MAX(`item_number`) FROM wishlists WHERE `chat_id` = ? AND `topic` = ?", (chat_id, topic))
    max_item_number = cursor.fetchone()[0]
    cursor.execute("UPDATE wishlists SET `item_number` = `item_number` - 1 WHERE `item_number` BETWEEN ? AND ?",
                   (item_number + 1, max_item_number))
    connection.commit()
    bot.send_message(message.chat.id,
                     "Your item has been successfully deleted. Use /open_wishlist to see all items in your wishlist")


bot.infinity_polling()
