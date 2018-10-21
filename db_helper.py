from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float
from credentials import db_user, db_password, db_host, db_port, db_database
from models import restaurant
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = 'postgres://{user}:{password}@{host}:{port}/{database}'.format(user     = db_user,
                                                                                         password = db_password,
                                                                                         host     = db_host,
                                                                                         port     = db_port,
                                                                                         database = db_database)
engine = create_engine(SQLALCHEMY_DATABASE_URI, encoding='UTF8', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()

restaurants = Table('restaurants', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('rest_type', String),
    Column('adress', String),
    Column('rc_link', String),
    Column('rc_rating', Float)
)

metadata.create_all(engine)
mapper(restaurant.Restaurant, restaurants)


def add_restauraunts(rest_list):
    pass

