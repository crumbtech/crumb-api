from contextlib import contextmanager

import sqlalchemy as sa
import sqlalchemy.orm as orm
import faker

import src.config as config

POSTGRES = {
    'database': config.for_env.POSTGRES_NAME,
    'drivername': 'postgres',
    'host': config.for_env.POSTGRES_HOST,
    'port': config.for_env.POSTGRES_PORT,
    'username': config.for_env.POSTGRES_USER,
    'password': config.for_env.POSTGRES_PASS,
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
    fake = faker.Factory.create()
    with session_manager() as session:
        for _ in range(0, 5):
            fake_number = '+1' + fake.phone_number()
            session.add(Crumb(status=CRUMB_STATUSES['ACTIVE']))
            session.add(User(first_name=fake.first_name(),
                             last_name=fake.last_name(),
                             phone_number=fake_number))
