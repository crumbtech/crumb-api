from contextlib import contextmanager

import sqlalchemy as sa
import sqlalchemy.orm as orm
import faker

from src.config import config_for_env as config

POSTGRES = {
    'database': config.POSTGRES_NAME,
    'drivername': 'postgres',
    'host': config.POSTGRES_HOST,
    'port': config.POSTGRES_PORT,
    'username': config.POSTGRES_USER,
    'password': config.POSTGRES_PASS,
}

postgres_url = str(sa.engine.url.URL(**POSTGRES))
engine = sa.engine.create_engine(postgres_url)
Session = orm.sessionmaker(bind=engine)


@contextmanager
def db_session():
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
    from src.models.crumb import Crumb, CRUMB_STATUSES
    from src.models.user import User
    fake = faker.Factory.create()
    with db_session() as session:
        for _ in range(0, 5):
            fake_number = '+1' + fake.phone_number()
            session.add(Crumb(status=CRUMB_STATUSES['ACTIVE']))
            session.add(User(first_name=fake.first_name(),
                             last_name=fake.last_name(),
                             phone_number=fake_number))
