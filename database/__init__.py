from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

SETTINGS = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5000',
    'username': 'postgres',
    'password': 'postgres',
}

engine = create_engine(URL(**SETTINGS), echo=True)
