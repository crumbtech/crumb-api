import random

import pytest
import faker

from src.app import create_app
from src.database import db_session
from src.models import Crumb, User
from src.lib import normalize_phone_number

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
    return normalize_phone_number(phone_number)


@pytest.fixture
def user_dict(first_name, last_name, phone_number):
    return dict(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number)


@pytest.fixture
def user(user_dict):
    user_instance = User(**user_dict)
    with db_session() as session:
        session.add(user_instance)
        session.commit()
        yield user_instance
        session.delete(user_instance)


@pytest.fixture
def confirmed_user(user_dict):
    user_instance = User(**user_dict)
    with db_session() as session:
        session.add(user_instance)
        code = user_instance.confirmation_code
        user_instance.confirm_phone_number_with_code(code)
        session.add(user_instance)
        session.commit()
        yield user_instance
        session.delete(user_instance)


@pytest.fixture
def crumb_dict():
    return dict()


@pytest.fixture
def crumb(crumb_dict):
    crumb_instance = Crumb(**crumb_dict)
    with db_session() as session:
        session.add(crumb_instance)
        session.commit()
        yield crumb_instance
        session.delete(crumb_instance)


@pytest.fixture
def crumb_image_dict(user, crumb):
    return dict(
        user_id=user.id,
        crumb_id=crumb.id,
        s3_url=fake.image_url())


@pytest.fixture
def test_client():
    app = create_app()
    return app.test_client()
