from contextlib import contextmanager

import sqlalchemy as sa
import sqlalchemy.orm as orm

import src.config as config
cfg = config.config_for_env

POSTGRES = {
    'database': cfg.POSTGRES_NAME,
    'drivername': 'postgres',
    'host': cfg.POSTGRES_HOST,
    'port': cfg.POSTGRES_PORT,
    'username': cfg.POSTGRES_USER,
    'password': cfg.POSTGRES_PASS,
}

postgres_url = str(sa.engine.url.URL(**POSTGRES))
engine = sa.engine.create_engine(postgres_url)
Session = orm.sessionmaker(bind=engine)


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
    from src.models import Crumb, CRUMB_STATUSES, User
    with session_manager() as session:
        for _ in range(0, 5):
            session.add(Crumb(status=CRUMB_STATUSES['ACTIVE']))
            session.add(User(phone_number='+19876543', password='password'))
