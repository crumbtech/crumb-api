import random
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
    first_name = sa.Column(sa.Text, nullable=False)
    last_name = sa.Column(sa.Text, nullable=False)
    confirmation_code = sa.Column(sa.Text, nullable=False)
    phone_number_confirmed = sa.Column(sa.Boolean, nullable=False,
                                       default=False)
    phone_number = sa.Column(sa.Text, unique=True, nullable=False)

    def __init__(self, **kwargs):
        self.first_name = kwargs.pop('first_name')
        self.last_name = kwargs.pop('last_name')
        self.phone_number_confirmed = False
        self.confirmation_code = str(random.randint(10000, 99999))
        self.phone_number = lib.normalize_phone_number(
            kwargs.pop('phone_number'))

    @staticmethod
    def decode_user_id_from_auth_token(token):
        """ extracts user_id from jwt auth token
        """
        try:
            return lib.decode_jwt_token(token)['sub']
        except ValueError:
            return None

    def send_confirmation_code(self):
        lib.send_sms_message(self.phone_number,
                             "Your Crumb confirmation code is {}".format(
                                 self.confirmation_code))

    def generate_auth_token(self):
        assert self.phone_number_confirmed is True
        return lib.generate_jwt_token_for_subject(self.id)

    def check_confirmation_code(self, confirmation_code):
        return self.confirmation_code == confirmation_code

    def confirm_phone_number_with_code(self, confirmation_code):
        self.phone_number_confirmed = False
        if self.check_confirmation_code(confirmation_code):
            self.phone_number_confirmed = True


class Crumb(TrackedTableMixin, BaseModel):
    __tablename__ = 'crumbs'
    id = sa.Column(sa.Integer, primary_key=True)
    status = sa.Column(sa.Enum(CRUMB_STATUSES['ACTIVE'],
                               CRUMB_STATUSES['ENDED'],
                               name='crumb_statuses'),
                       nullable=False,
                       default=CRUMB_STATUSES['ACTIVE'])

    crumb_images = sa.orm.relationship('CrumbImage')


class CrumbImage(TrackedTableMixin, BaseModel):
    __tablename__ = 'crumb_images'
    id = sa.Column(sa.Integer, primary_key=True)
    crumb_id = sa.Column(sa.Integer, sa.ForeignKey('crumbs.id'),
                         nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    s3_url = sa.Column(sa.Text, nullable=False)

    crumb = sa.orm.relationship('Crumb', back_populates='crumb_images')
    user = sa.orm.relationship('User')
