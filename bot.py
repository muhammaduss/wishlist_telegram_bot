import sqlite3

from config import bot

connection = sqlite3.connect('wishlists.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS wishlists (chat_id INTEGER, topic TEXT, item TEXT, item_number INTEGER)")
connection.commit()


@bot.message_handler(commands=['start'])
def start_message(message):
    # Greeting of user
    greeting = f'Hello, {message.from_user.first_name}!'
    bot.send_message(message.chat.id, greeting)

    # TODO: write list of commands
    bot.send_message(message.chat.id, 'What you want to do?')


@bot.message_handler(commands=['add'])
def add_command(message):
    bot.send_message(message.chat.id, 'Write topic name:')
    message_for_user = 'Write item which you want to add to chosen topic:'
    operation = 'add'
    bot.register_next_step_handler(message, get_topic_name, message_for_user, operation)


@bot.message_handler(commands=['delete'])
def delete_command(message):
    bot.send_message(message.chat.id, 'Write topic name:')
    message_for_user = 'Write number of item which you want to delete from chosen topic:'
    operation = 'delete'
    bot.register_next_step_handler(message, get_topic_name, message_for_user, operation)


@bot.message_handler(commands=['open_wishlist'])
def open_wishlist_command(message):
    bot.send_message(message.chat.id, 'Write topic name:')
    operation = 'open_wishlist'
    message_for_user = 'One moment, please...'
    bot.register_next_step_handler(message, get_topic_name, message_for_user, operation)


@bot.message_handler(commands=['new_wishlist'])
def new_wishlist_command(message):
    bot.send_message(message.chat.id, 'Write name of your wishlist which you want to create:')
    message_for_user = 'Creating...'
    operation = 'new_wishlist'
    bot.register_next_step_handler(message, get_topic_name, message_for_user, operation)


def get_topic_name(message, message_for_user, operation):
    topic = message.text
    bot.send_message(message.chat.id, message_for_user)
    if operation == 'add':
        bot.register_next_step_handler(message, add_item, topic)
    elif operation == 'open_wishlist':
        open_existing_wishlist(message, topic)
    elif operation == 'new_wishlist':
        create_new_wishlist(message, topic)
    else:
        bot.register_next_step_handler(message, delete_item, topic)


def open_existing_wishlist(message, topic):
    chat_id = message.chat.id
    cursor.execute("SELECT * FROM wishlists WHERE chat_id = ? AND topic = ?", (chat_id, topic))
    items = cursor.fetchall()
    if len(items) == 0:
        bot.send_message(message.chat.id, "Sorry, seems like you don't have such wishlist, please rewrite or "
                                          "create wishlist with this topic as a /new_wishlist")
    elif len(items) == 1:
        bot.send_message(message.chat.id, "Success! But your wishlist is empty.\n "
                                          "You can add items to it, using /add command")
    else:
        response = "Here are the items in your wishlist:\n"
        for item in items:
            if item[2] is not None and item[3] is not None:
                response += f"{item[3]}. {item[2]}\n"

        bot.send_message(message.chat.id, response)


def create_new_wishlist(message, topic):
    chat_id = message.chat.id
    cursor.execute("INSERT INTO wishlists VALUES (?, ?, NULL, NULL)", (chat_id, topic))
    connection.commit()
    bot.send_message(message.chat.id, 'Congratulations, your wishlist has been added! Now you can add items or delete'
                                      ' them using this commands: /add and /delete ')


def add_item(message, topic):
    chat_id = message.chat.id
    item = message.text
    cursor.execute("SELECT * FROM wishlists WHERE `chat_id` = ? AND `topic` = ?", (chat_id, topic))
    item_number = len(cursor.fetchall())
    cursor.execute("INSERT INTO wishlists VALUES (?, ?, ?, ?)", (chat_id, topic, item, item_number))
    connection.commit()


def delete_item(message, topic):
    chat_id = message.chat.id
    item_number = int(message.text)

    cursor.execute("DELETE FROM wishlists WHERE `chat_id` = ? AND `topic` = ? AND `item_number` = ?",
                   (chat_id, topic, item_number))
    connection.commit()

    cursor.execute("SELECT MAX(`item_number`) FROM wishlists WHERE `chat_id` = ? AND `topic` = ?", (chat_id, topic))
    max_item_number = cursor.fetchone()[0]
    cursor.execute("UPDATE wishlists SET `item_number` = `item_number` - 1 WHERE `item_number` BETWEEN ? AND ?",
                   (item_number + 1, max_item_number))
    connection.commit()


bot.infinity_polling()
