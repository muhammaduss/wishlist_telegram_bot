import sqlite3

from telebot import types
from config import bot

connection = sqlite3.connect('wishlists.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS wishlists (chat_id INTEGER, topic TEXT, item TEXT, item_number INTEGER)")


@bot.message_handler(commands=['start'])
def start_message(message):
    # Greeting of user
    greeting = f'Hello, {message.from_user.first_name}!'
    bot.send_message(message.chat.id, greeting)

    # Showing buttons
    markup = types.ReplyKeyboardMarkup()
    new_wishlist = types.KeyboardButton('Create new wishlist')
    existing_wishlist = types.KeyboardButton('Open existing wishlist')
    markup.add(new_wishlist, existing_wishlist)
    bot.send_message(message.chat.id, 'What you want to do?', reply_markup=markup)


@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, 'Write topic name:')
    message_for_user = 'Write item which you want to add to chosen topic:'
    operation = 'add'
    bot.register_next_step_handler(message, get_topic_name, message_for_user, operation)


@bot.message_handler(commands=['delete'])
def delete(message):
    bot.send_message(message.chat.id, 'Write topic name:')
    message_for_user = 'Write number of item which you want to delete from chosen topic:'
    operation = 'delete'
    bot.register_next_step_handler(message, get_topic_name, message_for_user, operation)


@bot.message_handler(content_types=['text'])
def handler(message):
    if message.text == "Create new wishlist":
        bot.send_message(message.chat.id, 'Write name of your wishlist:', reply_markup=types.ReplyKeyboardRemove())

        bot.register_next_step_handler(message, create_new_wishlist)
    elif message.text == "Open existing wishlist":
        bot.send_message(message.chat.id, 'One moment, please...')


def create_new_wishlist(message):
    chat_id = message.chat.id
    topic = message.text
    cursor.execute("INSERT INTO wishlists VALUES (?, ?, NULL, NULL)", (chat_id, topic))
    connection.commit()
    bot.send_message(message.chat.id, 'Congratulations, your wishlist has been added! Now you can add items or delete'
                                      ' them using this commands: /add and /delete ')


def get_topic_name(message, message_for_user, operation):
    topic = message.text
    bot.send_message(message.chat.id, message_for_user)
    if operation == 'add':
        bot.register_next_step_handler(message, add_item, topic)
    else:
        bot.register_next_step_handler(message, delete_item, topic)


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
