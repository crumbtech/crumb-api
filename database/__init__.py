import sqlalchemy as sa

SETTINGS = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5000',
    'username': 'postgres',
    'password': 'postgres',
}

engine = sa.create_engine(sa.engine.url.URL(**SETTINGS), echo=True)
