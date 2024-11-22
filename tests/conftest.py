# Fixtures here will be available in all tests
import pytest

from tests.setup.test_db import reset_test_db


@pytest.fixture(scope='module', autouse=True)
def reset_database():
    reset_test_db()
