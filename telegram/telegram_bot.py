import sys
import time
import telebot
from telebot import types
import logging
from credentials import TELEGRAM_TOKEN
from telegram import rests_management


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except AttributeError as err:
            error_handler_private(args[0], err, 'AttributeError')
        except KeyError as err:
            error_handler_private(args[0], err, 'KeyError')
        except ValueError as err:
            error_handler_private(args[0], err, 'ValueError')
        except TypeError as err:
            error_handler_private(args[0], err, 'TypeError')
        return result
    return wrapper


def error_handler_private(call, err, type_of_err):
    bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
    get_main_menu(call.message)
    logging.error(u'Method: ' + sys._getframe().f_code.co_name + ' ' + type_of_err + ' ' + str(err))


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
@bot.callback_query_handler(func=lambda call: call.data == 'next-restaurant')
@error_handler
def get_random_restaurant(call):
    message = rests_management.det_random_restaurant()
    message.edit_message_text(bot, call)


# BOT POLLING
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception:
        time.sleep(5)
        continue

