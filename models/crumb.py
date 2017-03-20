import sqlalchemy as sa
from models.base import BaseModel, TrackedTableMixin


class Crumb(TrackedTableMixin, BaseModel):
    __tablename__ = 'crumbs'
    id = sa.Column(sa.Integer, primary_key=True)
