class ContactType(object):

    def __init__(self, cont_type_id, description):
        self.cont_type_id = cont_type_id                  # ID
        self.description = description  # Описание

    def __repr__(self):
        return "<ContactType('%s', '%s')>" % (self.cont_type_id, self.description)