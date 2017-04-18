import random

import pytest
import faker

from src.app import create_app
import src.database as db
import src.models as models
import src.lib as lib

fake = faker.Factory.create()


@pytest.fixture
def first_name():
    return fake.first_name()


@pytest.fixture
def last_name():
    return fake.last_name()


@pytest.fixture
def phone_number():
    return '+1' + str(random.randint(1000000000, 9999999999))


@pytest.fixture
def normalized_phone_number(phone_number):
    return lib.normalize_phone_number(phone_number)


@pytest.fixture
def user_dict(first_name, last_name, phone_number):
    return dict(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number)


@pytest.fixture
def user(user_dict):
    user_instance = models.User(**user_dict)
    with db.session_manager() as session:
        session.add(user_instance)
        session.commit()
        yield user_instance
        session.delete(user_instance)


@pytest.fixture
def confirmed_user(user_dict):
    user_instance = models.User(**user_dict)
    with db.session_manager() as session:
        session.add(user_instance)
        code = user_instance.confirmation_code
        user_instance.confirm_phone_number_with_code(code)
        session.add(user_instance)
        session.commit()
        yield user_instance
        session.delete(user_instance)


@pytest.fixture
def test_client():
    app = create_app()
    return app.test_client()
