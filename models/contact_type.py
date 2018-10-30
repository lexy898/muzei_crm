class ContactType(object):

    def __init__(self, cont_type_id, description, rating = None):
        self.cont_type_id = cont_type_id   # ID
        self.description = description     # Описание
        self.rating = rating               # Рейтинг контакта с данным типом

    def __repr__(self):
        return "<ContactType('%s', '%s')>" % (self.cont_type_id, self.description)