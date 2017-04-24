import random
import sqlalchemy as sa

from src.models.base import TrackedTableMixin, BaseModel
from src.lib import (normalize_phone_number, decode_jwt_token,
                     send_sms_message, generate_jwt_token_for_subject)


class User(TrackedTableMixin, BaseModel):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text, nullable=False)
    last_name = sa.Column(sa.Text, nullable=False)
    confirmation_code = sa.Column(sa.Text, nullable=False)
    phone_number_confirmed = sa.Column(sa.Boolean, nullable=False,
                                       default=False)
    phone_number = sa.Column(sa.Text, unique=True, nullable=False)

    crumb_images = sa.orm.relationship('CrumbImage', back_populates='user')

    def __init__(self, **kwargs):
        self.first_name = kwargs.pop('first_name')
        self.last_name = kwargs.pop('last_name')
        self.phone_number_confirmed = False
        self.confirmation_code = str(random.randint(10000, 99999))
        self.phone_number = normalize_phone_number(
            kwargs.pop('phone_number'))

    @staticmethod
    def decode_user_id_from_auth_token(token):
        """ extracts user_id from jwt auth token
        """
        try:
            return decode_jwt_token(token)['sub']
        except ValueError:
            return None

    def send_confirmation_code(self):
        send_sms_message(self.phone_number,
                         "Your Crumb confirmation code is {}".format(
                             self.confirmation_code))

    def generate_auth_token(self):
        assert self.phone_number_confirmed is True
        return generate_jwt_token_for_subject(self.id)

    def check_confirmation_code(self, confirmation_code):
        return self.confirmation_code == confirmation_code

    def confirm_phone_number_with_code(self, confirmation_code):
        self.phone_number_confirmed = False
        if self.check_confirmation_code(confirmation_code):
            self.phone_number_confirmed = True
