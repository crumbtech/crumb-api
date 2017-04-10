import json

from src.app import create_app
import src.database as db
import src.models as models


class TestAuthView:
    user_dict = dict(phone_number='+12345678', password='test')

    def delete_existing_users(self):
        with db.session_manager() as session:
            for user in session.query(models.User):
                session.delete(user)

    def register_user(self):
        app = create_app()
        client = app.test_client()
        res = client.post(
            '/auth/register',
            data=json.dumps(self.user_dict),
            content_type='application/json')
        return res

    def test_register_with_new_user(self):
        self.delete_existing_users()
        res = self.register_user()
        data = json.loads(res.data.decode())
        assert res.status_code == 200
        assert data['auth_token'] is not None

    def test_register_with_existing_user(self):
        self.delete_existing_users()
        with db.session_manager() as session:
            session.add(models.User(**self.user_dict))
        res = self.register_user()
        data = json.loads(res.data.decode())
        assert res.status_code == 202
        assert data.get('auth_token') is None
