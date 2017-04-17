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
        token = persisted_user.generate_auth_token()
        assert isinstance(token, str) is True
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
