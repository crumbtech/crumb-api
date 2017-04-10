import src.lib as lib


def test_encode_jwt_token():
    token = lib.encode_jwt_token({'sub': 'test'})
    assert type(token) == bytes


def test_generate_jwt_token_for_subject():
    token = lib.generate_jwt_token_for_subject('test')
    assert type(token) == str
