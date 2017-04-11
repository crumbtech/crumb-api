import bcrypt

import src.database as db
import src.models as models


class TestUser:
    user_dict = dict(phone_number='+12345678910', password='test')

    def test_hash_password(self):
        """ successfully hashes password
        """
        hashed = models.User.hash_password('password', bcrypt.gensalt())
        assert type(hashed) == bytes

    def test_verify_password(self):
        """ correctly tests passwords against the hashed password in the database
        """
        user = models.User(**self.user_dict)
        with db.session_manager() as session:
            session.add(user)
            session.commit()
            user.verify_password(self.user_dict['password'])

    def test_create_user(self):
        """ successfully creates a user record
        """
        user = models.User(**self.user_dict)
        with db.session_manager() as session:
            session.add(user)
            session.commit()
            persisted_user = session.query(models.User).filter_by(
                    phone_number=self.user_dict['phone_number']).first()
            assert type(persisted_user.id) == int
            token = persisted_user.generate_auth_token()
            assert type(token) == str
            session.delete(persisted_user)
