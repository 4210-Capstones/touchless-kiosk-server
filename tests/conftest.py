# Fixtures here will be available in all tests
import os
os.environ['RUNNING_TESTS'] = 'true'

from tests.setup.dependency_overrides import override_get_db
from tests.setup.objects import user_schema
from tests.setup.test_db import get_test_db

import pytest
from starlette.testclient import TestClient

from backend.database.Service import UserService
from backend.database.dependency_db import get_db
from backend.main import app

from tests.setup.test_db import reset_test_db


@pytest.fixture(scope='module', autouse=True)
def reset_database():
    reset_test_db()


@pytest.fixture(scope='module')
def client():
    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


@pytest.fixture(scope="module")
def user_id(client):
    """
    Creates new user, yields id, deletes user after test is finished.
    """

    ret = client.post("/users", json=user_schema.model_dump())

    assert ret.status_code == 201

    with get_test_db() as db:
        user = UserService.get_by_mail(user_schema.user_email, db)

    assert user.user_email == user_schema.user_email
    assert user.user_password != user_schema.user_password

    yield user.id

    with get_test_db() as db:
        UserService.delete(user.id, db)


@pytest.fixture(scope="module")
def user_access_header(user_id, client):
    """
    Logs user in. Returns the header, which should be sent as authentication to user-protected endpoints.
    """

    form_data = {"username": user_schema.user_email, "password": user_schema.user_password}

    response = client.post("/login", data=form_data)

    assert response.status_code == 200
    assert "access_token" in response.json()

    return {"Authorization": "Bearer " + response.json()["access_token"]}
