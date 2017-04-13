import bcrypt
import pytest
import sqlalchemy

import src.models as models
import src.database as db


def test_hash_password(password):
    """ successfully hashes password
    """
    hashed = models.User.hash_password(password, bcrypt.gensalt())
    assert type(hashed) == bytes


def test_verify_password(phone_number, password):
    """ correctly tests passwords against the hashed password in the database
    """
    user = models.User(phone_number=phone_number, password=password)
    with db.session_manager() as session:
        session.add(user)
        session.commit()
        assert user.verify_password('invalid password') is False
        assert user.verify_password(password) is True
        session.delete(user)


def test_create_user(normalized_phone_number, password):
    """ successfully creates a user record
    """
    user = models.User(phone_number=normalized_phone_number, password=password)
    with db.session_manager() as session:
        session.add(user)
        session.commit()
        persisted_user = session.query(models.User).filter_by(
            phone_number=normalized_phone_number).one()
        assert isinstance(persisted_user.id, int) is True
        token = persisted_user.generate_auth_token()
        assert isinstance(token, str) is True
        session.delete(persisted_user)


def test_create_duplicate_user(phone_number, password):
    """ the database should not let us insert duplicate phone numbers
    """
    user1 = models.User(phone_number=phone_number, password=password)
    user2 = models.User(phone_number=phone_number, password=password)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        with db.session_manager() as session:
            session.add(user1)
            session.commit()
            session.add(user2)
            session.commit()
            session.delete(user1)
            session.delete(user2)
