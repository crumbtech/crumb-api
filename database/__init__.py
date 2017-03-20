from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker

CONFIG = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': 'postgres',
}

engine = engine.create_engine(engine.url.URL(**CONFIG), echo=True)
Session = sessionmaker(bind=engine)
