"""
All database classes will be declared here
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declared_attr

from database.config_db import BASE

from sqlalchemy import create_engine, inspect
#from database.config_db import ENGINE  # Import your database engine


class DBParentClass(BASE):
    """
    The base class for all database classes.
    It automatically declares the table name, adds a column for a unique id and provides to_dict and __str__ functions.

    Usage:

    class ConcreateClass(DBParentClass):
        __abstract__ = False

        # continue implementation
    """

    __abstract__ = True

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    # id = Column(Integer, primary_key=True, index=True)

    def to_dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

    def __str__(self):
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("%s=%s" % item for item in vars(self).items())
        )


class User(DBParentClass):
    __abstract__ = False

    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)   # store hashed, not plain

class Roles(DBParentClass):
    __abstract__ = False

    role_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    role_name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)

class UserRoles(DBParentClass):
    __abstract__ = False

    user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    role_id = Column(Integer, ForeignKey(Roles.role_id), primary_key=True)

class Service(DBParentClass):
    __abstract__ = False

    S_RoomNumber = Column(Integer, primary_key=True, nullable=False, unique=False)
    S_Name = Column(String(50), nullable=False)

class Booking(DBParentClass):
    __abstract__ = False

    B_StartDate = Column(DateTime, primary_key=True, nullable=False, unique=False)
    B_EndDate = Column(DateTime, nullable=False, unique=False)
    B_UserID = Column(Integer, ForeignKey(User.user_id), primary_key=True, nullable=False, unique=True)
    B_Name = Column(String(50), nullable=False)
    B_RoomNumber = Column(Integer, ForeignKey(Service.S_RoomNumber), primary_key=True, unique=False)

# # Inspect and list tables
# def list_tables():
#     inspector = inspect(ENGINE)  # ENGINE should be the SQLAlchemy engine instance
#     tables = inspector.get_table_names()
#     return tables

# if __name__ == "__main__":
#     print("Tables in the database:")
#     print(list_tables())
