import bcrypt

import src.database as db
import src.models as models


class TestUser:
    def test_hash_password(self):
        hashed = models.User.hash_password('password', bcrypt.gensalt())
        assert type(hashed) == bytes

    def test_create_user(self):
        phone_number = '+12345678'
        user = models.User(phone_number=phone_number, password='password')
        with db.session_manager() as session:
            session.add(user)
            session.commit()
            persisted_user = session.query(models.User).filter_by(
                    phone_number=phone_number).first()
            assert type(persisted_user.id) == int
            token = persisted_user.generate_auth_token()
            assert type(token) == str
            session.delete(persisted_user)
