import json

from src.app import create_app
from src.database import db_session
from src.models import User


def register_user(user_dict):
    """ make a request to the register endpoint to create a new user
    """
    app = create_app()
    test_client = app.test_client()
    res = test_client.post(
        '/auth/register',
        data=json.dumps(user_dict),
        content_type='application/json')
    return res


def test_register_with_new_user(user_dict):
    """ register a user that doesn't already exist
    """
    res = register_user(user_dict)
    # lets go ahead and delete this user now that we have the response info
    # we need so we don't muck up the test database
    with db_session() as session:
        session.query(User).filter_by(
            phone_number=user_dict['phone_number']).delete()
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert data.get('auth_token') is None
    assert data.get('user_id') is not None
    assert data.get('first_name') == user_dict['first_name']
    assert data.get('last_name') == user_dict['last_name']


def test_register_with_existing_user(user, user_dict):
    """
    attempt to register a user that already exists. ensure we return a
    status code that indicates the client needs to log in
    """
    res = register_user(user_dict)
    # we don't need to delete the user created here by the request to the
    # /auth/register endpoint because the it will be deleted in the
    # pytest teardown of the user fixture. pytest fixtures are only
    # run once per test, so user_dict has the same info as the user
    # instance because the user instance fixture depends on the
    # user_dict fixture.
    data = json.loads(res.data.decode())
    assert res.status_code == 202
    assert data['message'] == 'already-exists'
    assert data.get('auth_token') is None


def test_request_with_auth_token(test_client, confirmed_user):
    """
    make a request to the server with an auth token. ensure that the
    server is able to decode the auth token and fetch the correct user
    from the database
    """
    auth_token = confirmed_user.generate_auth_token()
    res = test_client.get(
        '/auth/current-user',
        headers=dict(Authorization='Bearer ' + auth_token))
    user_data = json.loads(res.data.decode())
    assert user_data['id'] == confirmed_user.id


def test_login_with_valid_credentials(test_client, user_dict):
    user = User(**user_dict)
    with db_session() as session:
        session.add(user)
    res = test_client.post(
        '/auth/login',
        data=json.dumps(user_dict),
        content_type='application/json')
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert data.get('auth_token') is None
    assert data['user_id'] is not None


def test_login_with_invalid_phone(test_client, user):
    res = test_client.post(
        '/auth/login',
        data=json.dumps(dict(
            phone_number='+19876543210')),
        content_type='application/json')
    data = json.loads(res.data.decode())

    assert res.status_code == 401
    assert data['message'] == 'no-user-for-phone'
    assert data.get('auth_token') is None


def test_confirm_user_with_valid_code(test_client, user):
    res = test_client.post(
        '/auth/confirm',
        data=json.dumps(dict(
            user_id=user.id,
            confirmation_code=user.confirmation_code)),
        content_type='application/json')
    data = json.loads(res.data.decode())

    assert res.status_code == 200
    assert data.get('auth_token') is not None


def test_confirm_user_with_invalid_code(test_client, user):
    res = test_client.post(
        '/auth/confirm',
        data=json.dumps(dict(
            user_id=user.id,
            confirmation_code='invalid code')),
        content_type='application/json')
    data = json.loads(res.data.decode())

    assert res.status_code == 401
    assert data.get('auth_token') is None
    assert data.get('message') == 'invalid-code'


def test_get_presigned_image_upload_url_without_confirmed_user(test_client):
    res = test_client.get('/auth/presigned-image-upload-url')
    data = json.loads(res.data.decode())

    assert res.status_code == 401
    assert data.get('message') == 'authentication-required'


def test_get_presigned_image_upload_url_with_confirmed_user(test_client,
                                                            confirmed_user):
    auth_token = confirmed_user.generate_auth_token()
    res = test_client.get(
        '/auth/presigned-image-upload-url',
        headers=dict(Authorization='Bearer ' + auth_token))
    data = json.loads(res.data.decode())

    assert res.status_code == 200
    assert data.get('presigned_url') is not None
    assert data.get('s3_url') is not None
