from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker

from config import POSTGRES
from models import Crumb


engine = engine.create_engine(engine.url.URL(**POSTGRES), echo=True)
Session = sessionmaker(bind=engine)


def seed_database():
    session = Session()

    for num in range(0, 100):
        session.add(Crumb())

    session.commit()
