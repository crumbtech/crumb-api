from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class Crumb(BaseModel):
    __tablename__ = 'crumbs'

    id = Column(Integer, primary_key=True)
