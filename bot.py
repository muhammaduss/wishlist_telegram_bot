import telebot
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
def adding(message):
    bot.send_message(message.chat.id, 'Write topic name:')
    bot.register_next_step_handler(message, get_topic_name)


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


def get_topic_name(message):
    topic = message.text
    bot.send_message(message.chat.id, 'Write item which you want to add for chosen topic:')
    bot.register_next_step_handler(message, add_item, topic)


def add_item(message, topic):
    chat_id = message.chat.id
    item = message.text
    cursor.execute("SELECT * FROM wishlists WHERE `chat_id` = ? AND `topic` = ?", (chat_id, topic))
    item_number = len(cursor.fetchall())
    cursor.execute("INSERT INTO wishlists VALUES (?, ?, ?, ?)", (chat_id, topic, item, item_number))
    connection.commit()


bot.infinity_polling()
