import models.contact
import db_helper


def add_contact(cont):
    contacts = db_helper.get_contacts_by_restaurant_id(cont.rest_id, cont.cont_type)
    cont_values_list = [i.cont_value for i in contacts]
    if cont.cont_type == 'PHONE':
        lol = check_phone_presence(cont_values_list, cont.cont_value)
        if not check_phone_presence(cont_values_list, cont.cont_value):
            db_helper.add_contact(cont)
    else:
        if cont.cont_value not in cont_values_list:
            db_helper.add_contact(cont)


def clear_phone(phone):
    import re
    return re.sub("\D", "", phone)


def check_phone_presence(cont_values_list, phone):
    presense = False
    phone = clear_phone(phone)
    c_cont_values_list = [clear_phone(i) for i in cont_values_list]
    for c_cont_value in c_cont_values_list:
        if phone in c_cont_value or c_cont_value in phone:
            presense = True
            break
    return presense