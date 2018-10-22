from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, DateTime
from credentials import db_user, db_password, db_host, db_port, db_database
from models import restaurant
from models import contact
from models import contact_type
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = 'postgres://{user}:{password}@{host}:{port}/{database}'.format(user=db_user,
                                                                                         password=db_password,
                                                                                         host=db_host,
                                                                                         port=db_port,
                                                                                         database=db_database)
engine = create_engine(SQLALCHEMY_DATABASE_URI, encoding='UTF8', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()

restaurants = Table('restaurants', metadata,
                    Column('rest_id', Integer, primary_key=True),
                    Column('name', String),
                    Column('rest_type', String),
                    Column('adress', String),
                    Column('rc_link', String),
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
                 Column('rest_id', Integer, ForeignKey("restaurants.rest_id"), nullable=False)
                 )

metadata.create_all(engine)

# ***mapping block***
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
