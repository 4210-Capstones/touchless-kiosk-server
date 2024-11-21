"""
All database classes will be declared here
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declared_attr, relationship

from database.config_db import BASE


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
    user_email = Column(String(100), unique=True, nullable=False)
    user_first = Column(String(100), nullable=False)
    user_last = Column(String(100), nullable=False)
    user_password = Column(String(255), nullable=False)   # store hashed, not plain

    user_roles = relationship("Role", secondary="userrole", back_populates="users")

class Role(DBParentClass):
    __abstract__ = False

    role_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    role_name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)

    users = relationship("User", secondary="userrole", back_populates="user_roles")

class UserRole(DBParentClass):
    __abstract__ = False

    user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    role_id = Column(Integer, ForeignKey(Role.role_id), primary_key=True)

class Tag(DBParentClass):
    __abstract__ = False

    tag_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    tag_name = Column(String(50), nullable=False)
    tag_description = Column(String, nullable=True)

    images = relationship("Image", secondary="imagetag", back_populates="tags")

class Image(DBParentClass):
    __abstract__ = False

    image_link = Column(String, primary_key=True, unique=True, nullable=False)

    image_requests = relationship("ImageRequest", back_populates="images")
    tags = relationship("Tag", secondary="imagetag", back_populates="images")

class ImageTag(DBParentClass):
    __abstract__ = False

    image_link = Column(String, ForeignKey(Image.image_link), primary_key=True)
    tag_id = Column(Integer, ForeignKey(Tag.tag_id), primary_key=True)

class Room(DBParentClass):
    __abstract__ = False

    room_number = Column(Integer, primary_key=True, nullable=False, unique=True)
    room_available = Column(Boolean, nullable=False, unique=False)

    bookings = relationship("Booking", secondary="bookingroom", back_populates="rooms")
    
class BookingType(DBParentClass):
    __abstract__ = False

    bookingtype_id = Column(Integer, primary_key=True, nullable=False, unique=False)
    bookingtype_name = Column(String(50), nullable=False)
    bookingtype_description = Column(String(255), nullable=False)
    
class Booking(DBParentClass):
    __abstract__ = False

    booking_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    bookingtype_id = Column(Integer, ForeignKey(BookingType.bookingtype_id), unique=False)
    booking_startdate = Column(DateTime, nullable=False, unique=False)
    booking_enddate = Column(DateTime, nullable=False, unique=False)
    booking_userid = Column(Integer, ForeignKey(User.user_id), nullable=False, unique=True)

    rooms = relationship("Room", secondary="BookingRoom", back_populates="bookings")

class BookingRoom(DBParentClass):
    __abstract__ = False

    bookingroom_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    booking_id = Column(Integer, ForeignKey(Booking.booking_id))
    room_number = Column(Integer, ForeignKey(Room.room_number))


class ImageRequest(DBParentClass):
    __abstract__ = False

    imgreq_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    imgreq_name = Column(String(50), nullable=False)
    imgreq_email = Column(String(100), unique=True, nullable=False)
    imgreq_message = Column(String, nullable=False)
    imgreq_link = Column(String, ForeignKey(Image.image_link), nullable=False)
    imgreq_startdate = Column(DateTime, nullable=False, unique=False)
    imgreq_enddate = Column(DateTime, nullable=False, unique=False)

    images = relationship("Image", back_populates="image_requests")


class Club(DBParentClass):
    __abstract__ = False

    club_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    club_name = Column(String(50), nullable=False, unique=True)
    club_description = Column(String, nullable=True)
    club_upcoming_activities = Column(String, nullable=True)

    requests = relationship("ClubRequest", back_populates="clubs")

class ClubRequest(DBParentClass):
    __abstract__ = False

    clubreq_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    clubreq_name = Column(String(50), nullable=False)
    clubreq_email = Column(String(100), nullable=False)
    clubreq_date = Column(DateTime, default=datetime.utcnow())
    club_id = Column(Integer, ForeignKey(Club.club_id), nullable=False)

    clubs = relationship("Club", back_populates="requests")

# # Inspect and list tables
# def list_tables():
#     inspector = inspect(ENGINE)  # ENGINE should be the SQLAlchemy engine instance
#     tables = inspector.get_table_names()
#     return tables

# if __name__ == "__main__":
#     print("Tables in the database:")
#     print(list_tables())
