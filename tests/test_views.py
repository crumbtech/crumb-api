import json
import pytest

from src.app import create_app
import src.database as db
import src.models as models


def register_user(user_dict):
    """ make a request to the register endpoint to create a new user record
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
    with db.session_manager() as session:
        session.query(models.User).filter_by(
            phone_number=user_dict['phone_number']).delete()
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert data.get('auth_token') is not None
    assert data.get('first_name') == user_dict['first_name']
    assert data.get('last_name') == user_dict['last_name']


def test_register_with_existing_user(user, user_dict):
    """ attempt to register a user that already exists. ensure we return a
    status code indicating the client needs to log in
    """
    res = register_user(user_dict)
    # we don't need to delete the user created here by the request to the
    # /auth/register endpoint because the it will be deleted in the
    # pytest teardown of the user fixture pytest fixtures are only
    # run once per test, so user_dict has the same info as the user
    # instance because the user instance fixture depends on the
    # user_dict fixture.
    data = json.loads(res.data.decode())
    assert res.status_code == 202
    assert data['status'] == 'already-exists'
    assert data.get('auth_token') is None


def test_request_with_auth_token(test_client, user):
    """ make a request to the server with an auth token. ensure that the
    server is able to decode the auth token and fetch the correct user
    from the database
    """
    auth_token = user.generate_auth_token()
    res = test_client.get(
        '/auth/current-user',
        headers=dict(Authorization='Bearer ' + auth_token))
    user_data = json.loads(res.data.decode())
    assert user_data['phone_number'] == user.phone_number


def test_login_with_valid_credentials(test_client, user_dict):
    user = models.User(**user_dict)
    with db.session_manager() as session:
        session.add(user)
    res = test_client.post(
        '/auth/login',
        data=json.dumps(user_dict),
        content_type='application/json')
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert data['auth_token'] is not None


def test_login_with_invalid_password(test_client, user):
    res = test_client.post(
        '/auth/login',
        data=json.dumps(dict(
            phone_number=user.phone_number,
            password='invalid password')),
        content_type='application/json')
    data = json.loads(res.data.decode())
    assert res.status_code == 401
    assert data['status'] == 'invalid-password'
    assert data.get('auth_token') is None


def test_login_with_invalid_phone(test_client, user_dict):
    with db.session_manager() as session:
        user = models.User(**user_dict)
        session.add(user)
        session.commit()

        res = test_client.post(
            '/auth/login',
            data=json.dumps(dict(
                password=user_dict['password'],
                phone_number='+19876543210')),
            content_type='application/json')
        data = json.loads(res.data.decode())

        assert res.status_code == 401
        assert data['status'] == 'no-user-for-phone'
        assert data.get('auth_token') is None

        session.delete(user)
