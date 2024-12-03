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
    availability_tutor: Mapped["AvailabilityTutor"] = relationship(back_populates="tutor_info")
    booking_tutor: Mapped["BookingTutor"] = relationship(back_populates="tutor_info", foreign_keys="[BookingTutor.bookingtutor_tutorid]")
    booking_student: Mapped["BookingTutor"] = relationship(back_populates="student_info", foreign_keys="[BookingTutor.bookingtutor_studentid]")

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

class ScheduleType(DBParentClass):
    __abstract__ = False

    # id: Mapped[int] = mapped_column(primary_key=True)
    scheduletype_name = Column(String(50), nullable=False)
    scheduletype_description = Column(String(150), nullable=False)

    schedules: Mapped[List["Schedule"]] = relationship(back_populates="schedule_type")

class RepeatRule(DBParentClass):
    __abstract__ = False

    # id: Mapped[int] = mapped_column(primary_key=True)
    repeatrule_name = Column(String(150), nullable=False, unique=True)
    repeatrule_description = Column(String(150), nullable=False)

    schedules: Mapped[List["Schedule"]] = relationship(back_populates="repeat_rule")

# Schedule table
class Schedule(DBParentClass):
    __abstract__ = False

    # id: Mapped[int] = mapped_column(primary_key=True)
    schedule_name = Column(String(50), nullable=False)  # Event name or description
    schedule_start_time = Column(DateTime, nullable=False)
    schedule_end_time = Column(DateTime, nullable=True)
    schedule_scheduletype_id = Column(Integer, ForeignKey("scheduletype.id"), nullable=False)
    schedule_repeatrule_id = Column(Integer, ForeignKey("repeatrule.id"), nullable=True)

    schedule_type: Mapped["ScheduleType"] = relationship(back_populates="schedules")
    repeat_rule: Mapped["RepeatRule"] = relationship(back_populates="schedules")
    booking_rooms: Mapped[List["BookingRoom"]] = relationship(back_populates="schedule")
    booking_tutors: Mapped[List["BookingTutor"]] = relationship(back_populates="schedule")
    availability_rooms: Mapped[List["AvailabilityRoom"]] = relationship(back_populates="schedule")
    availability_tutors: Mapped[List["AvailabilityTutor"]] = relationship(back_populates="schedule")

class Room(DBParentClass):
    __abstract__ = False

    room_number = Column(Integer, nullable=False, unique=True)
    room_available = Column(Boolean, nullable=False)

    availability_rooms : Mapped[List["AvailabilityRoom"]] = relationship(back_populates="room")
    booking_rooms : Mapped[List["BookingRoom"]] = relationship(back_populates="room")

class AvailabilityRoom(DBParentClass):
    __abstract__ = False

    # bookingroom_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    availability_room_number = Column(Integer, ForeignKey(Room.room_number))
    availability_room_schedule_id = Column(Integer, ForeignKey("schedule.id"), nullable=False)

    schedule: Mapped["Schedule"] = relationship(back_populates="availability_rooms")
    room: Mapped["Room"] = relationship(back_populates="availability_rooms")

class AvailabilityTutor(DBParentClass):
    __abstract__ = False

    # bookingroom_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    availabilitytutor_schedule_id = Column(Integer, ForeignKey("schedule.id"), nullable=False)
    availabilitytutor_tutorid = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)

    schedule: Mapped["Schedule"] = relationship(back_populates="availability_tutors")
    tutor_info: Mapped["User"] = relationship(back_populates="availability_tutor")
    

class BookingRoom(DBParentClass):
    __abstract__ = False

    # bookingroom_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    bookingroom_number = Column(Integer, ForeignKey(Room.room_number))
    bookingroom_schedule_id = Column(Integer, ForeignKey("schedule.id"), nullable=False)

    schedule: Mapped["Schedule"] = relationship(back_populates="booking_rooms")
    room: Mapped["Room"] = relationship(back_populates="booking_rooms")

class BookingTutor(DBParentClass):
    __abstract__ = False

    # bookingroom_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    bookingtutor_schedule_id = Column(Integer, ForeignKey("schedule.id"), nullable=False)
    bookingtutor_tutorid = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)
    bookingtutor_studentid =  Column(Integer, ForeignKey(User.id), nullable=False)

    schedule: Mapped["Schedule"] = relationship(back_populates="booking_tutors")
    tutor_info: Mapped["User"] = relationship(foreign_keys=[bookingtutor_tutorid], back_populates="booking_tutor")
    student_info: Mapped["User"] = relationship(foreign_keys=[bookingtutor_studentid], back_populates="booking_student")
    

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
# inspector = inspect(ENGINE)  # ENGINE should be the SQLAlchemy engine instance
# tables = inspector.get_table_names()
# return tables
# if __name
#  == "__main":
# print("Tables in the database:")
# print(list_tables())