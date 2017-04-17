import bcrypt
import pytest
import sqlalchemy

import src.models as models
import src.database as db


def test_create_user(user_dict):
    """ successfully creates a user record
    """
    user = models.User(**user_dict)
    with db.session_manager() as session:
        session.add(user)
        session.commit()
        persisted_user = session.query(models.User).filter_by(
            phone_number=user_dict['phone_number']).one()
        assert isinstance(persisted_user.id, int) is True
        session.delete(persisted_user)


def test_create_duplicate_user(user_dict):
    """ the database should not let us insert duplicate phone numbers
    """
    user1 = models.User(**user_dict)
    user2 = models.User(**user_dict)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        with db.session_manager() as session:
            session.add(user1)
            session.commit()
            session.add(user2)
            session.commit()
            session.delete(user1)
            session.delete(user2)


def test_user_confirmed_defaults_to_false(user):
    assert user.phone_number_confirmed is False


def test_check_confirmation_code(user):
    confirmation_code = user.confirmation_code
    assert user.check_confirmation_code(confirmation_code) is True
    assert user.check_confirmation_code('invalid code') is False


def test_confirm_phone_number_with_code(user):
    confirmation_code = user.confirmation_code
    user.confirm_phone_number_with_code(confirmation_code)
    assert user.phone_number_confirmed is True
    user.confirm_phone_number_with_code('invalid code')
    assert user.phone_number_confirmed is False


def test_unconfirmed_user_cannot_generate_auth_token(user):
    assert user.phone_number_confirmed is False
    with pytest.raises(AssertionError):
        user.generate_auth_token()
