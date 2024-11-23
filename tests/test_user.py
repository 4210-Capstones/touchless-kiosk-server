import os
os.environ['RUNNING_TESTS'] = 'true'

from tests.setup.objects import user_schema


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