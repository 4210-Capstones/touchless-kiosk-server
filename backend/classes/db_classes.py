"""
All database classes will be declared here
"""
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declared_attr, relationship

from database.config_db import BASE

from sqlalchemy import create_engine, inspect
from datetime import datetime
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

    user_roles = relationship("UserRole", back_populates="users")

class Role(DBParentClass):
    __abstract__ = False

    role_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    role_name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)

class UserRole(DBParentClass):
    __abstract__ = False

    user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    role_id = Column(Integer, ForeignKey(Role.role_id), primary_key=True)

    users = relationship("User", back_populates="user_roles")

class Service(DBParentClass):
    __abstract__ = False

    service_roomnumber = Column(Integer, primary_key=True, nullable=False, unique=False)
    service_name = Column(String(50), nullable=False)

class Booking(DBParentClass):
    __abstract__ = False

    booking_startdate = Column(DateTime, primary_key=True, nullable=False, unique=False)
    booking_enddate = Column(DateTime, nullable=False, unique=False)
    booking_userid = Column(Integer, ForeignKey(User.user_id), primary_key=True, nullable=False, unique=True)
    booking_name = Column(String(50), nullable=False)
    booking_email = Column(String(100), unique=True, nullable=False)
    booking_roomnumber = Column(Integer, ForeignKey(Service.service_roomnumber), primary_key=True, unique=False)

class Image(DBParentClass):
    __abstract__ = False

    image_link = Column(String, primary_key=True, nullable=False)

class Club(DBParentClass):
    __abstract__ = False

    club_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    club_name = Column(String, nullable=False, unique=True)
    club_description = Column(String, nullable=True)
    club_upcoming_activities = Column(String, nullable=True)

    requests = relationship("ClubRequest", back_populates="club")

class ClubRequest(DBParentClass):
    __abstract__ = False

    clubreq_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    clubreq_name = Column(String, nullable=False)
    clubreq_email = Column(String, nullable=False)
    clubreq_date = Column(DateTime, default=datetime.utcnow())
    club_id = Column(Integer, ForeignKey(Club.club_id), nullable=False)

    club = relationship("Club", back_populates="requests")

# class Tutoring(DBParentClass):
    
    
# # Inspect and list tables
# def list_tables():
#     inspector = inspect(ENGINE)  # ENGINE should be the SQLAlchemy engine instance
#     tables = inspector.get_table_names()
#     return tables

# if __name__ == "__main__":
#     print("Tables in the database:")
#     print(list_tables())
