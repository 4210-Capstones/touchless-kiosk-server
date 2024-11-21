from tests.setup.test_db import get_test_db


def override_get_db():
    with get_test_db() as db:
        yield db