import os

from tests.setup.dependency_overrides import override_get_db
from tests.setup.objects import user_schema
from tests.setup.test_db import get_test_db

os.environ['RUNNING_TESTS'] = 'true'

import pytest
from starlette.testclient import TestClient

from backend.database.Service import UserService
from backend.database.dependency_db import get_db
from backend.main import app

@pytest.fixture(scope='module')
def client():
    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


@pytest.fixture(scope="module")
def user_id(client):
    ret = client.post("/users", json=user_schema.model_dump())

    assert ret.status_code == 201

    with get_test_db() as db:
        user = UserService.get_by_mail(user_schema.user_email, db)

    assert user.user_email == user_schema.user_email
    assert user.user_password != user_schema.user_password

    yield user.user_id

    with get_test_db() as db:
        UserService.delete(user.user_id, db)


@pytest.fixture(scope="module")
def user_access_header(user_id, client):
    with get_test_db() as db:
        form_data = {"username": UserService.get(user_id, db).user_email, "password": user_schema.user_password}

    response = client.post("/login", data=form_data)

    assert response.status_code == 200
    assert "access_token" in response.json()

    return {"Authorization": "Bearer " + response.json()["access_token"]}


def test_create_user(user_id):
    # The test is implemented in the fixture
    pass


def test_create_user_again(user_id, client):
    ret = client.post("/users", json=user_schema.model_dump())

    assert ret.status_code == 409


def test_get_user(user_access_header, client):
    response = client.get("users/profile", headers=user_access_header)

    assert response.status_code == 200
    assert response.json()["user_email"] == user_schema.user_email