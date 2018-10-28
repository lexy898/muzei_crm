import db_helper
from telebot import types
from telegram import message as msg


def get_random_restaurant():
    restaurant = db_helper.get_random_restaurant()
    message = msg.Message('', None)
    message.add_message_row(restaurant.name, font_style='Bold')
    message.add_message_row(restaurant.rest_type)
    message.add_message_row(restaurant.adress)
    message.add_message_row(restaurant.rc_link)
    contacts = db_helper.get_contacts_by_restaurant_id(restaurant.rest_id)
    for contact in contacts:
        if contact.cont_type == 'PHONE':
            message.add_message_row('📞' + contact.cont_value + ' ' + contact.description)
        elif contact.cont_type == 'E-MAIL':
            message.add_message_row('✉' + contact.cont_value + ' ' + contact.description)
        else:
            message.add_message_row(contact.cont_value + ' ' + contact.description)
    markup = types.InlineKeyboardMarkup()
    row = [types.InlineKeyboardButton("Отправить e-mail", callback_data="send-email"),
           types.InlineKeyboardButton("Следующий>", callback_data="next-restaurant")]
    markup.row(*row)
    message.markup = markup
    return message