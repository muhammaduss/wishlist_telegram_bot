import telebot
import sqlite3

token = '6251500867:AAGTuIRrbxjA5e566Bsne3eElPNR7Xmi1vU'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello! How I can help you? You can choose from buttons below!')
