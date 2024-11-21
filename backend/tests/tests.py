import os

import pytest
from starlette.testclient import TestClient

from classes.schemas import UserSchema
from database.Service import UserService
from database.dependency_db import get_db
from main import app
from tests.setup.dependency_overrides import override_get_db

os.environ['RUNNING_TESTS'] = 'true'

@pytest.fixture(scope='module')
def client():
    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)

user_schema = UserSchema(email='user@example.com', password='12345678')
@pytest.fixture(scope="module")
def user_id(client):
    ret = client.post("/users", json=user_schema.model_dump())

    assert ret.status_code == 201

    db = next(override_get_db())
    user = UserService.get_by_mail(user_schema.email, db)

    assert user.email == user_schema.email
    assert user.password != user_schema.password

    return user.user_id


@pytest.fixture(scope="module")
def user_access_header(user_id, client):
    form_data = {"username": user_id, "password": user_schema.password}

    response = client.post("/users/login", data=form_data)

    assert response.status_code == 200
    assert "access_token" in response.json()

    return {"Authorization": "Bearer " + response.json()["access_token"]}


def test_create_user(user_id):
    # The test is implemented in the fixture
    pass

def test_get_user(user_access_header, client):
    response = client.get("users/profile", headers=user_access_header)

    assert response.status_code == 200
    assert response.json().email == user_schema.email