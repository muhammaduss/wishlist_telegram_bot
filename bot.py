import telebot
import sqlite3

from telebot import types
from config import bot
from db import BotDatabase

bot_db = BotDatabase('wishlist.db')


# cursor.execute()

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


@bot.message_handler(content_types=['text'])
def handler(message):
    if message.text == "Create new wishlist":
        bot.send_message(message.chat.id, 'Creating...')
    elif message.text == "Open existing wishlist":
        bot.send_message(message.chat.id, 'One moment, please...')


bot.infinity_polling()
