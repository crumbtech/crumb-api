import bcrypt
import pytest
import sqlalchemy
import faker

import src.models as models
import src.database as db
import src.lib as lib


fake = faker.Factory.create()


def test_hash_password():
    """ successfully hashes password
    """
    hashed = models.User.hash_password('password', bcrypt.gensalt())
    assert type(hashed) == bytes


def test_verify_password():
    """ correctly tests passwords against the hashed password in the database
    """
    test_password = 'password'
    user = models.User(phone_number='+12345678910', password=test_password)
    with db.session_manager() as session:
        session.add(user)
        session.commit()
        assert user.verify_password('invalid password') is False
        assert user.verify_password(test_password) is True


def test_create_user():
    """ successfully creates a user record
    """
    test_phone = lib.normalize_phone_number('+1' + fake.phone_number())
    user = models.User(phone_number=test_phone, password='password1')
    with db.session_manager() as session:
        session.add(user)
        session.commit()
        persisted_user = session.query(models.User).filter_by(
            phone_number=test_phone).one()
        assert isinstance(persisted_user.id, int) is True
        token = persisted_user.generate_auth_token()
        assert isinstance(token, str) is True
        session.delete(persisted_user)


def test_create_duplicate_user():
    """ the database should not let us insert duplicate phone numbers
    """
    user1 = models.User(phone_number='+12345678910', password='password1')
    user2 = models.User(phone_number='+12345678910', password='password2')
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        with db.session_manager() as session:
            session.add(user1)
            session.commit()
            session.add(user2)
            session.commit()
            session.delete(user1)
            session.delete(user2)
