from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from database.config_db import engine


def get_db():
    """
    Gets the current database connection, closes database connection after operation is finished.

    This will be used by API endpoints as dependency to pass down database session.

    Usage:
    @[router_name].[operation: get, post, etc.]("/[url]", ...)
    async def f(..., db: Session = Depends(get_db)):
        ...
        some_function(..., db)
        ...
    """

    try:
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        yield db
    finally:
        db.close()


db_context = contextmanager(get_db)
