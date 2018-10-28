class Contact(object):

    def __init__(self, cont_value, description, cont_type, added_date, update_date, rest_id, source):
        self.cont_value = cont_value    # Контактные данные
        self.description = description  # Описание
        self.cont_type = cont_type      # Тип контактных данных
        self.added_date = added_date    # Дата добавления
        self.update_date = update_date  # Дата обновления
        self.rest_id = rest_id          # ИД заведения
        self.source = source            # Источник

    def __repr__(self):
        return "<Contact('%s', '%s', '%s', '%s', '%s', '%s')>" % \
               (self.cont_value, self.description, self.cont_type, self.added_date, self.update_date, self.rest_id)
