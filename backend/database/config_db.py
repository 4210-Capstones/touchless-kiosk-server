import inspect
import os
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

import configuration

# some necessary configuration
database_url = configuration.database_url
engine = create_engine(database_url, echo=False)    # the database engine, essentially the central communication point
BASE = declarative_base()   # all database classes will inherit from BASE


def create_db():
    """
    Creates database and tables if not existing yet.
    """

    if not database_exists(engine.url):
        create_database(engine.url)

    BASE.metadata.create_all(engine)


def autocommit(func):
    """
    Function decorator to automatically commit the session after executing the function and to automatically rollback on error.

    Usage: (See Service.py)

    @autocommit
    def f(..., db: Session):    # db session will be passed down from API as dependency to have a fresh session for each request.
        # do your stuff

        db.commit()
        return ...
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # inspect arguments to find the one of type Session
        bound_args = inspect.signature(func).bind(*args, **kwargs)
        db_session = None
        for name, value in bound_args.arguments.items():
            if isinstance(value, Session):
                db_session = value
                break

        if not db_session:
            raise ValueError("A db_session of type Session must be provided to the decorated function.")

        try:
            result = func(*args, **kwargs)
            db_session.commit()     # Commit changes if function executes successfully
            return result
        except SQLAlchemyError as e:
            # TODO: Log error
            db_session.rollback()
            raise e

    return wrapper
