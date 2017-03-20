import sqlalchemy as sa

from base import BaseModel


class Crumb(BaseModel):
    __tablename__ = 'crumbs'

    id = sa.Column(sa.Integer, primary_key=True)
