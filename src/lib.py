import flask
import jwt
import phonenumbers

import src.config as config


def encode_jwt_token(payload):
    return jwt.encode(payload, config.for_env.JWT_SECRET, algorithm='HS256')


def generate_jwt_token_for_subject(sub):
    payload = {'sub': sub}
    encoded_token = encode_jwt_token(payload)
    return encoded_token.decode()


def decode_jwt_token(token):
    try:
        return jwt.decode(token, config.for_env.JWT_SECRET)
    except jwt.exceptions.DecodeError:
        raise ValueError('invalid token')


def normalize_phone_number(phone_number):
    parsed = phonenumbers.parse(phone_number)
    normalized = phonenumbers.format_number(
        parsed,
        phonenumbers.PhoneNumberFormat.E164,
    )

    length = len(normalized)
    # possible length range of E164 formatted phone numbers.
    # international numbers can be longer than 10 digits
    # plus sign + country code + ten digit number = 12 characters
    assert length >= 12 and length <= 17

    return normalized


def send_sms_message(number, message):
    if config.for_env.CRUMB_ENV == 'prod':
        # send code in SMS message
        pass
    else:
        # output to server log when in dev environment
        flask.current_app.logger.info(message)
