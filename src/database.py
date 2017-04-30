from contextlib import contextmanager
import random

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
    from src.models import Crumb, CrumbImage
    from src.models.crumb import CRUMB_STATUSES
    from src.models.user import User
    fake = faker.Factory.create()
    with db_session() as session:
        for _ in range(0, 5):
            fake_number = '+1' + str(random.randint(1000000000, 9999999999))
            crumb = Crumb(status=CRUMB_STATUSES['ACTIVE'])
            user = User(first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        phone_number=fake_number)
            session.add(crumb)
            session.add(user)
            session.commit()
            crumb_image = CrumbImage(crumb_id=crumb.id,
                                     s3_url=fake.image_url(),
                                     user_id=user.id)
            session.add(crumb_image)
            session.commit()
