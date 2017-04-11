import datetime as dt
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
import bcrypt

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
    phone_number = sa.Column(sa.Text, nullable=False)
    password = sa.Column(sa.Text, nullable=False)
    password_salt = sa.Column(sa.Text, nullable=False)

    def __init__(self, **kwargs):
        self.phone_number = lib.normalize_phone_number(
                kwargs.pop('phone_number'))
        password_salt = bcrypt.gensalt()
        self.password = self.hash_password(
                kwargs.pop('password'), password_salt).decode()
        self.password_salt = password_salt.decode()

    @staticmethod
    def hash_password(password, salt):
        return bcrypt.hashpw(password.encode(), salt)

    @staticmethod
    def decode_auth_token(token):
        """ extracts user_id from jwt auth token
        """
        try:
            return lib.decode_jwt_token(token)['sub']
        except ValueError:
            return None

    def verify_password(self, supplied_password):
        computed = self.hash_password(supplied_password,
                                      self.password_salt.encode())
        return self.password.encode() == computed

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
