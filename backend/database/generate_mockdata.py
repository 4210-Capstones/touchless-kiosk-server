"""import os
from pathlib import Path
from backend.database.dependency_db import get_db
from backend.database.config_db import engine
from faker import Faker
from datetime import datetime, timedelta
import random

# Import your models
from backend.classes.db_classes import User, Role, UserRole, Tag, Image, ImageTag, Room, BookingType, Booking,BookingRoom, ImageRequest, Club, ClubRequest

# Initialize the Faker instance and database connection
faker = Faker()
db = next(get_db())

# Populate data
def create_fake_data():
    db.query(BookingRoom).delete()
    db.query(Room).delete()
    db.query(ImageRequest).delete()
    db.query(ImageTag).delete()
    db.query(Tag).delete()
    db.query(Image).delete()
    db.query(ClubRequest).delete()
    db.query(Club).delete()
    db.query(Booking).delete()
    db.query(BookingType).delete()
    db.query(UserRole).delete()
    db.query(Role).delete()
    db.query(User).delete()

    # Create roles
    roles = [
        Role(role_name='Student', role_description='Someone who attends classes and pays tuition'),
        Role(role_name='Admin', role_description='Administrator with full access to all features'),
        Role(role_name='Tutor', role_description='Responsible for guiding and assisting students in their learning process'),
        Role(role_name='Teaching Assistant', role_description='Helps teach newer students'),
        Role(role_name='Teacher', role_description='Responsible for planning, delivering lessons, and assessing student progress'),
        Role(role_name='Staff Member', role_description='Support and manage institutional operations and administrative tasks')
    ]
    for role in roles:
        db.add(role)
    db.commit()

    # Create users
    users = []
    for _ in range(10):
        user = User(
            user_email=faker.unique.email(),
            user_first=faker.first_name(),
            user_last=faker.last_name(),
            user_password=faker.password()
        )
        users.append(user)
        db.add(user)
    db.commit()

    # Assign random roles to users
    for user in users:
        assigned_roles = set()  # Keep track of roles already assigned to this user
        for _ in range(random.randint(1, 3)):
            while True:  # Ensure the role is unique for this user
                role = random.choice(roles)
                if role.id not in assigned_roles:
                    break  # Found a unique role for this user
            user_role = UserRole(
                user_id=user.id,
                role_id=role.id
            )
            db.add(user_role)
            assigned_roles.add(role.id)  # Mark this role as assigned
    db.commit()


    # Create tags
    tags = [
        Tag(tag_name="Hackathon", tag_description="Tag for Hackathon events"),
        Tag(tag_name="ACM", tag_description="Tag for ACM events"),
        Tag(tag_name="ACMW", tag_description="Tag for ACMW events"),
        Tag(tag_name="CTF", tag_description="Tag for CTF events"),
        Tag(tag_name="GDSC", tag_description="Tag for GDSC events"),
        Tag(tag_name="ICPC", tag_description="Tag for ICPC events"),
        Tag(tag_name="IEEE", tag_description="Tag for IEEE events"),
        Tag(tag_name="IGDA", tag_description="Tag for IGDA events"),
        Tag(tag_name="Robotics", tag_description="Tag for Robotics events"),
        Tag(tag_name="WebDev", tag_description="Tag for WebDev events"),
        Tag(tag_name="Workshops", tag_description="Tag for Workshops events"),
        Tag(tag_name="Jobs", tag_description="Tag for Jobs events"),
        Tag(tag_name="Research", tag_description="Tag for Research events")
    ]
    for tag in tags:
        db.add(tag)
    db.commit()

    # Directory containing images
    image_dir = Path("tests/test_images")

    # Specific images to be used
    image_filenames = ["test0.jpg", "test1.jpg", "test2.png", "test3.png", "test4.png", "test5.jpg", "test6.jpg", "test7.jpg", "test8.jpg"]


    # Create images and add them to the database
    images = []
    for filename in image_filenames:
        image_path = image_dir / filename
        if image_path.exists():
            new_image = Image(
                image_link=str(image_path),  # Store the image path as a link
                image_confirmed=faker.boolean()
            )
            images.append(new_image)
            db.add(new_image)
        else:
            print(f"Warning: Image file {filename} does not exist in {image_dir}. Skipping.")
    db.commit()

    # Assign tags to images
    for image in images:
        assigned_tags = set()  # To track already assigned tag IDs for the current image
        for _ in range(random.randint(1, 5)):
            tag = random.choice(tags)
            if tag.id not in assigned_tags:
                image_tag = ImageTag(
                    image_link=image.image_link,
                    tag_id=tag.id
                )
                db.add(image_tag)
                assigned_tags.add(tag.id)  # Mark this tag as assigned to the image
    db.commit()


    # Create rooms
    rooms = []
    for i in range(100, 360):
        room = Room(
            room_number=i,
            room_available=faker.boolean()
        )
        rooms.append(room)
        db.add(room)
    db.commit()

    # Create booking types
    booking_types = [
        BookingType(bookingtype_name="Room", bookingtype_description="Booking for rooms"),
        BookingType(bookingtype_name="Tutoring", bookingtype_description="Booking for tutoring"),
        BookingType(bookingtype_name="Office hours", bookingtype_description="Booking for office hours")
    ]
    for booking_type in booking_types:
        db.add(booking_type)
    db.commit()

    # Create bookings
    for _ in range(15):
        booking = Booking(
            bookingtype_id=random.choice(booking_types).id,
            booking_startdate=faker.date_time_this_year(),
            booking_enddate=faker.date_time_this_year(),
            booking_userid=random.choice(users).id
        )
        db.add(booking)
        db.commit()

        # Assign room to booking
        booking_room = BookingRoom(
            booking_id=booking.id,
            room_number=random.choice(rooms).room_number
        )
        db.add(booking_room)
    db.commit()

    # Create clubs
    clubs = [
        Club(club_name="ACM",      club_description="Tag for ACM events", club_upcoming_activities="Upcoming activity"),
        Club(club_name="ACMW",    club_description="Tag for ACMW events", club_upcoming_activities="Upcoming activity"),
        Club(club_name="CTF",      club_description="Tag for CTF events", club_upcoming_activities="Upcoming activity"),
        Club(club_name="GDSC",    club_description="Tag for GDSC events", club_upcoming_activities="Upcoming activity"),
        Club(club_name="ICPC",    club_description="Tag for ICPC events", club_upcoming_activities="Upcoming activity"),
        Club(club_name="IEEE",    club_description="Tag for IEEE events", club_upcoming_activities="Upcoming activity"),
        Club(club_name="IGDA",    club_description="Tag for IGDA events", club_upcoming_activities="Upcoming activity"),
        Club(club_name="Robotics", club_description="Tag for Robotics events", club_upcoming_activities="Upcoming activity"),
    ]
    for club in clubs:
        db.add(club)
    db.commit()

    # Create club requests
    for _ in range(10):
        club_request = ClubRequest(
            clubreq_name=faker.name(),
            clubreq_email=faker.email(),
            clubreq_date=faker.date_time_this_year(),
            club_id=random.choice(clubs).id
        )
        db.add(club_request)
    db.commit()

    # Create image requests
    for image in images:
        image_request = ImageRequest(
            imgreq_name=faker.name(),
            imgreq_email=faker.email(),
            imgreq_message=faker.text(),
            imgreq_link=image.image_link,
            imgreq_startdate=faker.date_time_this_year(),
            imgreq_enddate=faker.date_time_this_year()
        )
        db.add(image_request)
    db.commit()"""