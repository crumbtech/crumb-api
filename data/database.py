from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker

from data.config import POSTGRES
from data.models import Crumb

postgres_url = engine.url.URL(**POSTGRES)
engine = engine.create_engine(postgres_url, echo=True)
Session = sessionmaker(bind=engine)


def seed_database():
    session = Session()

    for num in range(0, 100):
        session.add(Crumb())

    session.commit()
