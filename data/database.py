from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker

from config import POSTGRES
from models import Crumb

postgres_url = str(engine.url.URL(**POSTGRES))
engine = engine.create_engine(postgres_url, echo=True)
Session = sessionmaker(bind=engine)


def seed_database():
    session = Session()

    for num in range(0, 100):
        session.add(Crumb())

    session.commit()
