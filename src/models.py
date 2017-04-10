import datetime as dt
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

import src.lib as lib

BaseModel = declarative_base()

CRUMB_STATUSES = {
    'ACTIVE': 'active',
    'ENDED': 'ended',
}


class TrackedTableMixin(object):
    date_created = sa.Column(sa.DateTime, nullable=False,
                             default=dt.datetime.utcnow)
    date_modified = sa.Column(sa.DateTime, nullable=False,
                              default=dt.datetime.utcnow,
                              onupdate=dt.datetime.utcnow)


class User(TrackedTableMixin, BaseModel):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)

    def generate_auth_token(self):
        return lib.generate_jwt_token_for_subject(self.id)


class Crumb(TrackedTableMixin, BaseModel):
    __tablename__ = 'crumbs'
    id = sa.Column(sa.Integer, primary_key=True)
    status = sa.Column(sa.Enum(CRUMB_STATUSES['ACTIVE'],
                               CRUMB_STATUSES['ENDED'],
                               name='crumb_statuses'),
                       nullable=False,
                       default=CRUMB_STATUSES['ACTIVE'])
