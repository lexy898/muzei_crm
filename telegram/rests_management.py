import db_helper
from telebot import types
from telegram import message as msg


def det_random_restaurant():
    restaurant = db_helper.get_random_restaurant()
    message = msg.Message('', None)
    message.add_message_row(restaurant.name, font_style='Bold')
    message.add_message_row(restaurant.rest_type)
    message.add_message_row(restaurant.adress)
    message.add_message_row(restaurant.rc_link)
    # message.add_message_row(restaurant.contacts)

    markup = types.InlineKeyboardMarkup()
    row = [types.InlineKeyboardButton("Отправить e-mail", callback_data="send-email"),
           types.InlineKeyboardButton("Следующий>", callback_data="next-restaurant")]
    markup.row(*row)
    message.markup = markup
    return message