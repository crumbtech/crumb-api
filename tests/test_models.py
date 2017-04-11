import bcrypt
import pytest
import sqlalchemy

import src.database as db
import src.models as models


class TestUser:
    user_dict = dict(phone_number='+12345678910', password='test')

    def delete_existing_users(self):
        """ delete all records from users table
        """
        with db.session_manager() as session:
            for user in session.query(models.User):
                session.delete(user)

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
            session.delete(user)

    def test_create_user(self):
        """ successfully creates a user record
        """
        user = models.User(**self.user_dict)
        with db.session_manager() as session:
            session.add(user)
            session.commit()
            persisted_user = session.query(models.User).filter_by(
                phone_number=self.user_dict['phone_number']).first()
            assert isinstance(persisted_user.id, int) is True
            token = persisted_user.generate_auth_token()
            assert isinstance(token, str) is True
            session.delete(persisted_user)

    def test_create_duplicate_user(self):
        """ the database should not let us insert duplicate phone numbers
        """
        self.delete_existing_users()
        user1 = models.User(**self.user_dict)
        user2 = models.User(**self.user_dict)
        with pytest.raises(sqlalchemy.exc.IntegrityError):
            with db.session_manager() as session:
                session.add(user1)
                session.commit()
                session.add(user2)
                session.commit()
                session.delete(user1)
                session.delete(user2)
