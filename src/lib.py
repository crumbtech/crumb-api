import uuid

import flask
import jwt
import phonenumbers
import boto3
from botocore.client import Config

from src.config import config_for_env as config


def encode_jwt_token(payload):
    return jwt.encode(payload, config.JWT_SECRET, algorithm='HS256')


def generate_jwt_token_for_subject(sub):
    payload = {'sub': sub}
    encoded_token = encode_jwt_token(payload)
    return encoded_token.decode()


def decode_jwt_token(token):
    try:
        return jwt.decode(token, config.JWT_SECRET)
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
    if config.SEND_SMS:
        sns = boto3.client('sns')
        sns.publish(PhoneNumber=number, Message=message)
    else:
        # output to server log when sms is disabled
        flask.current_app.logger.info(message)


def s3_client():
    return boto3.client('s3',
                        config=Config(signature_version='s3v4'),
                        region_name='us-east-1',
                        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)


def generate_presigned_image_upload_url(user_id, extension='.jpg'):
    """
    generate a presigned PUT url for s3 images bucket.
    create a random unique key name with extension for the new s3 object.
    prepends a uuid with user_id to ensure uniqueness of s3 key name - this
    is probably overkill but i don't want one user overwriting another's
    images in the s3 bucket so i'm going to play it safe.
    """
    s3 = s3_client()
    key_name = "{}-{}{}".format(user_id, uuid.uuid4().hex, extension)
    return s3.generate_presigned_url(
        'put_object',
        HttpMethod='PUT',
        Params=dict(Bucket=config.CRUMB_IMAGES_BUCKET_NAME,
                    Key=key_name))
