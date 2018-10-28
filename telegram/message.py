class Message:

    def __init__(self, text, markup):
        self.text = text
        self.markup = markup

    def add_message_row(self, text_row, font_style=None):
        if font_style == 'Bold':
            self.text += '<b>' + text_row + '</b>\n'
        else:
            self.text += text_row + '\n'

    def edit_message_text(self, bot, call):
        bot.edit_message_text(text=self.text,
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              reply_markup=self.markup,
                              parse_mode='HTML')