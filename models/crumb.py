import sqlalchemy as sa

from base import BaseModel


class Crumb(BaseModel):
    __tablename__ = 'crumbs'
