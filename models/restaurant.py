class Restaurant(object):

    def __init__(self, name, adress, rc_link, rc_rating, rest_type):
        self.name = name            # Название заведения
        self.rest_type = rest_type  # Тип заведения
        self.adress = adress        # Адрес заведения
        self.rc_link = rc_link      # Ссылка на Restoclub
        self.rc_rating = rc_rating  # Рейтинг на Restoclub
        self.contacts = []          # Список контактов

    def __repr__(self):
        return "<Restaurant('%s', '%s', '%s', '%s', '%s',)>" % \
               (self.name, self.rest_type, self.adress, self.rc_link, self.rc_rating)
