import pytest

import src.lib as lib


def test_encode_jwt_token():
    token = lib.encode_jwt_token({'sub': 'test'})
    assert type(token) == bytes


def test_generate_jwt_token_for_subject():
    token = lib.generate_jwt_token_for_subject('test')
    assert type(token) == str


def test_decode_jwt_token():
    valid_token = lib.generate_jwt_token_for_subject('test')
    invalid_token = 'invalid token'
    with pytest.raises(ValueError):
        lib.decode_jwt_token(invalid_token)
    lib.decode_jwt_token(valid_token)


def test_normalize_phone_number():
    invalid_number = '+1234567890'
    valid_number_a = '+1-234-567-8910'
    valid_number_b = '+1 234 567 8910'

    with pytest.raises(AssertionError):
        lib.normalize_phone_number(invalid_number)

    assert lib.normalize_phone_number(valid_number_a) == '+12345678910'
    assert lib.normalize_phone_number(valid_number_b) == '+12345678910'


def test_generate_presigned_image_upload_url(user):
    url = lib.generate_presigned_image_upload_url(user.id)
    assert isinstance(url, str)
