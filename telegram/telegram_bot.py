import time
import telebot
from telebot import types
import logging
from credentials import TELEGRAM_TOKEN
from telegram import rests_management


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Создание главного меню
@bot.message_handler(commands=['start'])
def get_main_menu(message):
    chat_id = message.chat.id
    message_text = 'MENU'
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Случайное заведение',
                                          callback_data='random-restaurant'))
    bot.send_message(chat_id, message_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'random-restaurant')
def get_random_restaurant(call):
    message = rests_management.det_random_restaurant()
    message.edit_message_text(bot, call)


# BOT POLLING
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception:
        time.sleep(15)
        continue

