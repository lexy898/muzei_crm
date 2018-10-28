from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, DateTime
from credentials import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE
from models import restaurant
from models import contact
from models import contact_type
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func

SQLALCHEMY_DATABASE_URI = 'postgres://{user}:{password}@{host}:{port}/{database}'.format(user=DB_USER,
                                                                                         password=DB_PASSWORD,
                                                                                         host=DB_HOST,
                                                                                         port=DB_PORT,
                                                                                         database=DB_DATABASE)
engine = create_engine(SQLALCHEMY_DATABASE_URI, encoding='UTF8', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()

restaurants = Table('restaurants', metadata,
                    Column('rest_id', Integer, primary_key=True),
                    Column('name', String),
                    Column('rest_type', String),
                    Column('adress', String),
                    Column('rc_link', String, unique=True),
                    Column('rc_rating', Float)
                    )

contact_types = Table('contact_types', metadata,
                      Column('cont_type_id', String, primary_key=True),
                      Column('description', String)
                      )

contacts = Table('contacts', metadata,
                 Column('cont_id', Integer, primary_key=True),
                 Column('cont_value', String, nullable=False),
                 Column('description', String),
                 Column('cont_type', String, ForeignKey("contact_types.cont_type_id"), nullable=False),
                 Column('added_date', DateTime, nullable=False),
                 Column('update_date', DateTime),
                 Column('rest_id', Integer, ForeignKey("restaurants.rest_id"), nullable=False),
                 Column('source', String)
                 )

metadata.create_all(engine)

'''
***************************
*******MAPPING BLOCK*******
***************************
'''
mapper(restaurant.Restaurant, restaurants)
mapper(contact_type.ContactType, contact_types)
mapper(contact.Contact, contacts)


def add_restauraunts(rest_list):
    session.add_all(rest_list)
    session.commit()

    contacts_list = []
    for rest in rest_list:
        for i in range(len(rest.contacts)):
            rest.contacts[i].rest_id = rest.rest_id
        contacts_list.extend(rest.contacts)

    session.add_all(contacts_list)
    session.commit()


def get_random_restaurant():
    query = session.query(restaurant.Restaurant).order_by(func.random()).limit(1)
    result = query.first()
    return result


def get_all_restaurants():
    query = session.query(restaurant.Restaurant)
    result = query.all()
    return result

def get_contacts_by_restaurant_id(restaurant_id):
    query = session.query(contact.Contact).filter(contact.Contact.rest_id == restaurant_id)
    result = query.all()
    return result
