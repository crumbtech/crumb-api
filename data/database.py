from contextlib import contextmanager

from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker

from data.config import POSTGRES
from data.models import Crumb

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
    with session_manager() as session:
        for num in range(0, 100):
            session.add(Crumb())
