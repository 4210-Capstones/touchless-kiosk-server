"""
All database classes will be declared here
"""
from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import declared_attr, relationship, Mapped

from backend.database.config_db import BASE


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

    id = Column(Integer, unique=True, index=True, primary_key=True, nullable=False, autoincrement=True)

    def to_dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

    def __str__(self):
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("%s=%s" % item for item in vars(self).items())
        )


class User(DBParentClass):
    __abstract__ = False

    # user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    user_email = Column(String(100), unique=True, nullable=False)
    user_first = Column(String(100), nullable=True)
    user_last = Column(String(100), nullable=True)
    user_password = Column(String(255), nullable=False)   # store hashed, not plain

    user_roles : Mapped[List["Role"]] = relationship(secondary="userrole", back_populates="users")

class Role(DBParentClass):
    __abstract__ = False

    # role_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    role_name = Column(String(50), nullable=False)
    role_description = Column(String(255), nullable=True)

    users : Mapped[List["User"]] = relationship(secondary="userrole", back_populates="user_roles")

class UserRole(DBParentClass):
    __abstract__ = False

    user_id = Column(Integer, ForeignKey(User.id))
    role_id = Column(Integer, ForeignKey(Role.id))

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uix_user_role"),
    )

class Tag(DBParentClass):
    __abstract__ = False

    # tag_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    tag_name = Column(String(50), nullable=False)
    tag_description = Column(String, nullable=True)

    images : Mapped[List["Image"]] = relationship(secondary="imagetag", back_populates="tags")

class Image(DBParentClass):
    __abstract__ = False

    image_link = Column(String, unique=True, nullable=False)
    image_confirmed = Column(Boolean, nullable=False)

    image_requests : Mapped[List["ImageRequest"]] = relationship(back_populates="images")
    tags : Mapped[List["Tag"]] = relationship(secondary="imagetag", back_populates="images")

class ImageTag(DBParentClass):
    __abstract__ = False

    image_link = Column(String, ForeignKey(Image.image_link))
    tag_id = Column(Integer, ForeignKey(Tag.id))

    __table_args__ = (
        UniqueConstraint("image_link", "tag_id", name="uix_image_tag"),
    )

class Room(DBParentClass):
    __abstract__ = False

    room_number = Column(Integer, nullable=False, unique=True)
    room_available = Column(Boolean, nullable=False)

    bookings : Mapped[List["Booking"]] = relationship(secondary="bookingroom", back_populates="rooms")
    
class BookingType(DBParentClass):
    __abstract__ = False

    # bookingtype_id = Column(Integer, primary_key=True, nullable=False, unique=False)
    bookingtype_name = Column(String(50), nullable=False)
    bookingtype_description = Column(String(255), nullable=True)
    
class Booking(DBParentClass):
    __abstract__ = False

    # booking_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    bookingtype_id = Column(Integer, ForeignKey(BookingType.id), unique=False)
    booking_startdate = Column(DateTime, nullable=False, unique=False)
    booking_enddate = Column(DateTime, nullable=False, unique=False)
    booking_userid = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)

    rooms : Mapped[List["Room"]] = relationship(secondary="BookingRoom", back_populates="bookings")

class BookingRoom(DBParentClass):
    __abstract__ = False

    # bookingroom_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    booking_id = Column(Integer, ForeignKey(Booking.id))
    room_number = Column(Integer, ForeignKey(Room.room_number))


class ImageRequest(DBParentClass):
    __abstract__ = False

    # imgreq_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    imgreq_name = Column(String(50), nullable=False)
    imgreq_email = Column(String(100), unique=True, nullable=False)
    imgreq_message = Column(String, nullable=False)
    imgreq_link = Column(String, ForeignKey(Image.image_link), nullable=False)
    imgreq_startdate = Column(DateTime, nullable=False, unique=False)
    imgreq_enddate = Column(DateTime, nullable=False, unique=False)

    images : Mapped[List["Image"]] = relationship(back_populates="image_requests")


class Club(DBParentClass):
    __abstract__ = False

    # club_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    club_name = Column(String(50), nullable=False, unique=True)
    club_description = Column(String, nullable=False)
    club_upcoming_activities = Column(String, nullable=True)

    requests : Mapped[List["ClubRequest"]] = relationship(back_populates="clubs")

class ClubRequest(DBParentClass):
    __abstract__ = False

    # clubreq_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    clubreq_name = Column(String(50), nullable=False)
    clubreq_email = Column(String(100), nullable=False)
    clubreq_date = Column(DateTime, default=datetime.utcnow())
    club_id = Column(Integer, ForeignKey(Club.id), nullable=False)

    clubs : Mapped[List["Club"]] = relationship(back_populates="requests")

# # Inspect and list tables
# def list_tables():
#     inspector = inspect(ENGINE)  # ENGINE should be the SQLAlchemy engine instance
#     tables = inspector.get_table_names()
#     return tables

# if __name__ == "__main__":
#     print("Tables in the database:")
#     print(list_tables())
