from contextlib import contextmanager

import sqlalchemy as sa
import sqlalchemy.orm as orm

import crumb_api.config as config

postgres_url = str(sa.engine.url.URL(**config.POSTGRES))
engine = sa.engine.create_engine(postgres_url, echo=True)
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
    from models import Crumb, CRUMB_STATUSES
    with session_manager() as session:
        for _ in range(0, 5):
            session.add(Crumb(status=CRUMB_STATUSES['ACTIVE']))
