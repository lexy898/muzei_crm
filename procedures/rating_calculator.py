import db_helper

restaurants = db_helper.get_all_restaurants()
ratings = db_helper.get_contact_types_raitings()

for restaurant in restaurants:
    rating = 0
    contacts = db_helper.get_contacts_by_restaurant_id(restaurant.rest_id)
    for cont in contacts:
        rating += ratings.get(cont.cont_type, 0)
    db_helper.update_rest_rating(restaurant.rest_id, rating)