from contextlib import contextmanager

from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker

import os

POSTGRES_NAME = os.environ.get('POSTGRES_NAME') or 'crumb_dev'
POSTGRES_HOST = os.environ.get('POSTGRES_HOST') or 'localhost'
POSTGRES_PORT = os.environ.get('POSTGRES_PORT') or '5432'
POSTGRES_USER = os.environ.get('POSTGRES_USER') or 'postgres'
POSTGRES_PASS = os.environ.get('POSTGRES_PASS') or 'postgres'

POSTGRES = {
    'database': POSTGRES_NAME,
    'drivername': 'postgres',
    'host': POSTGRES_HOST,
    'port': POSTGRES_PORT,
    'username': POSTGRES_USER,
    'password': POSTGRES_PASS,
}


postgres_url = str(engine.url.URL(**POSTGRES))
engine = engine.create_engine(postgres_url, echo=True)
Session = sessionmaker(bind=engine)


@contextmanager
def session_manager():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def seed_database():
    from models import Crumb, CRUMB_STATUSES
    with session_manager() as session:
        for _ in range(0, 5):
            session.add(Crumb(status=CRUMB_STATUSES['ACTIVE']))
