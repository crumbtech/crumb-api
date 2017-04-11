import json

from src.app import create_app
import src.database as db
import src.models as models


class TestAuthView:
    user_dict = dict(phone_number='+12345678', password='test')

    def delete_existing_users(self):
        """ delete all records from users table
        """
        with db.session_manager() as session:
            for user in session.query(models.User):
                session.delete(user)

    def register_user(self):
        """ make a request to the register endpoint to create a new user record
        """
        app = create_app()
        client = app.test_client()
        res = client.post(
            '/auth/register',
            data=json.dumps(self.user_dict),
            content_type='application/json')
        return res

    def test_register_with_new_user(self):
        """ register a user that doesn't already exist
        """
        self.delete_existing_users()
        res = self.register_user()
        data = json.loads(res.data.decode())
        assert res.status_code == 200
        assert data['auth_token'] is not None

    def test_register_with_existing_user(self):
        """ attempt to register a user that already exists. ensure we return a
        status code indicating the client needs to log in
        """
        self.delete_existing_users()
        with db.session_manager() as session:
            session.add(models.User(**self.user_dict))
        res = self.register_user()
        data = json.loads(res.data.decode())
        assert res.status_code == 202
        assert data.get('auth_token') is None

    def test_request_with_auth_token(self):
        """ make a request to the server with an auth token. ensure that the
        server is able to decode the auth token and fetch the correct user
        from the database
        """
        self.delete_existing_users()
        with db.session_manager() as session:
            user = models.User(**self.user_dict)
            session.add(user)
            session.commit()
            auth_token = user.generate_auth_token()
        app = create_app()
        client = app.test_client()
        res = client.get(
            '/auth/current-user',
            headers=dict(Authorization='Bearer ' + auth_token))
        user_data = json.loads(res.data.decode())
        assert user_data['phone_number'] == self.user_dict['phone_number']

    def test_login_with_valid_credentials(self):
        self.delete_existing_users()
        with db.session_manager() as session:
            user = models.User(**self.user_dict)
            session.add(user)
            session.commit()
        app = create_app()
        client = app.test_client()
        res = client.post(
            '/auth/login',
            data=json.dumps(self.user_dict),
            content_type='application/json')
        data = json.loads(res.data.decode())
        assert res.status_code == 200
        assert data['auth_token'] is not None

    def test_login_with_invalid_password(self):
        self.delete_existing_users()
        with db.session_manager() as session:
            user = models.User(**self.user_dict)
            session.add(user)
            session.commit()
        app = create_app()
        client = app.test_client()
        res = client.post(
            '/auth/login',
            data=json.dumps(dict(
                phone_number=self.user_dict['phone_number'],
                password='invalid password')),
            content_type='application/json')
        data = json.loads(res.data.decode())
        assert res.status_code == 401
        assert data['status'] == 'invalid-password'
        assert data.get('auth_token') is None

    def test_login_with_invalid_phone(self):
        self.delete_existing_users()
        with db.session_manager() as session:
            user = models.User(**self.user_dict)
            session.add(user)
            session.commit()
        app = create_app()
        client = app.test_client()
        res = client.post(
            '/auth/login',
            data=json.dumps(dict(
                password=self.user_dict['phone_number'],
                phone_number='+19876543')),
            content_type='application/json')
        data = json.loads(res.data.decode())
        assert res.status_code == 401
        assert data['status'] == 'no-user-for-phone'
        assert data.get('auth_token') is None
