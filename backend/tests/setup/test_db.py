from contextlib import contextmanager

from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from database.config_db import BASE

SQLALCHEMY_DATABASE_URL = "sqlite:///tests/test.db"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

if not database_exists(test_engine.url):
    create_database(test_engine.url)

# delete and create all tables
BASE.metadata.drop_all(bind=test_engine)
BASE.metadata.create_all(bind=test_engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def reset_test_db():
    BASE.metadata.drop_all(bind=test_engine)
    BASE.metadata.create_all(bind=test_engine)

@contextmanager
def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()