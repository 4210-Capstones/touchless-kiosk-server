from backend.database.dependency_db import get_db
from backend.database.config_db import engine
from faker import Faker
from datetime import datetime, timedelta
import random


# Import your models
from backend.classes.db_classes import (
    User, Role, UserRole, Tag, Image, ImageTag, Room, BookingRoom, ImageRequest, Club, ClubRequest,
    RepeatRule, ScheduleType, Schedule, BookingTutor, AvailabilityRoom, AvailabilityTutor
)

# Initialize the Faker instance and database connection
faker = Faker()
db = next(get_db())

def create_data():
    # Clear data except for static tables
    db.query(Room).delete()
    db.query(ImageRequest).delete()
    db.query(ImageTag).delete()
    db.query(Image).delete()
    db.query(ClubRequest).delete()
    db.query(Schedule).delete()
    db.query(BookingRoom).delete()
    db.query(BookingTutor).delete()
    db.query(AvailabilityRoom).delete()
    db.query(AvailabilityTutor).delete()

    # Ensure Roles remain static
    roles = [
        {"role_name": "Student", "role_description": "Someone who attends classes and pays tuition"},
        {"role_name": "Admin", "role_description": "Administrator with full access to all features"},
        {"role_name": "Tutor", "role_description": "Responsible for guiding and assisting students in their learning process"},
        {"role_name": "Teaching Assistant", "role_description": "Helps teach newer students"},
        {"role_name": "Teacher", "role_description": "Responsible for planning, delivering lessons, and assessing student progress"},
        {"role_name": "Staff Member", "role_description": "Support and manage institutional operations and administrative tasks"}
    ]
    for role_data in roles:
        if not db.query(Role).filter_by(role_name=role_data["role_name"]).first():
            db.add(Role(**role_data))
    db.commit()

    # Ensure Users remain static
    static_users = [
        {"user_email": "admin@example.com", "user_first": "Admin", "user_last": "User", "user_password": "securepassword"},
        {"user_email": "student@example.com", "user_first": "Student", "user_last": "User", "user_password": "securepassword"}
    ]
    for user_data in static_users:
        if not db.query(User).filter_by(user_email=user_data["user_email"]).first():
            db.add(User(**user_data))
    db.commit()

    # Ensure UserRoles remain static
    for user_data in static_users:
        user = db.query(User).filter_by(user_email=user_data["user_email"]).first()
        if user:
            if user.user_email == "admin@example.com":
                admin_role = db.query(Role).filter_by(role_name="Admin").first()
                if not db.query(UserRole).filter_by(user_id=user.id, role_id=admin_role.id).first():
                    db.add(UserRole(user_id=user.id, role_id=admin_role.id))
            elif user.user_email == "student@example.com":
                student_role = db.query(Role).filter_by(role_name="Student").first()
                if not db.query(UserRole).filter_by(user_id=user.id, role_id=student_role.id).first():
                    db.add(UserRole(user_id=user.id, role_id=student_role.id))
    db.commit()

    # Create tags
    tags = [
        {"tag_name": "Hackathon", "tag_description": "Tag for Hackathon events"},
        {"tag_name": "ACM", "tag_description": "Tag for ACM events"},
        {"tag_name": "ACMW", "tag_description": "Tag for ACMW events"},
        {"tag_name": "CTF", "tag_description": "Tag for CTF events"},
        {"tag_name": "GDSC", "tag_description": "Tag for GDSC events"},
        {"tag_name": "ICPC", "tag_description": "Tag for ICPC events"},
        {"tag_name": "IEEE", "tag_description": "Tag for IEEE events"},
        {"tag_name": "IGDA", "tag_description": "Tag for IGDA events"},
        {"tag_name": "Robotics", "tag_description": "Tag for Robotics events"},
        {"tag_name": "WebDev", "tag_description": "Tag for WebDev events"},
        {"tag_name": "Workshops", "tag_description": "Tag for Workshops events"},
        {"tag_name": "Jobs", "tag_description": "Tag for Jobs events"},
        {"tag_name": "Research", "tag_description": "Tag for Research events"}
    ]

    # Insert Tags
    for tag_data in tags:
        if not db.query(Tag).filter_by(tag_name=tag_data["tag_name"]).first():
            db.add(Tag(**tag_data))
    db.commit()

    # Create images
    images = []
    for _ in range(10):
        image = Image(
            image_link=faker.image_url(),
            image_confirmed=faker.boolean()
        )
        images.append(image)
        db.add(image)
    db.commit()
    
    # Assign tags to images
    for image in images:
        assigned_tags = set()  # To track already assigned tag IDs for the current image
        for _ in range(random.randint(1, 5)):
            tagQuery = db.query(Tag).get(random.randint(1, len(tags)))
            if tagQuery.id not in assigned_tags:
                image_tag = ImageTag(
                    image_link=image.image_link,
                    tag_id=tagQuery.id
                )
                db.add(image_tag)
                assigned_tags.add(tagQuery.id)  # Mark this tag as assigned to the image
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

    # Create clubs
    clubs = [
        {"club_name": "ACM", "club_description": "Association for Computing Machinery", "club_upcoming_activities": "Upcoming activity"},
        {"club_name": "ACMW", "club_description": "ACM Women in Computing", "club_upcoming_activities": "Upcoming activity"},
        {"club_name": "CTF", "club_description": "Capture the Flag cybersecurity club", "club_upcoming_activities": "Upcoming activity"},
        {"club_name": "GDSC", "club_description": "Google Developer Student Club", "club_upcoming_activities": "Upcoming activity"},
        {"club_name": "ICPC", "club_description": "International Collegiate Programming Contest", "club_upcoming_activities": "Upcoming activity"},
        {"club_name": "IEEE", "club_description": "Institute of Electrical and Electronics Engineers", "club_upcoming_activities": "Upcoming activity"},
        {"club_name": "IGDA", "club_description": "International Game Developers Association", "club_upcoming_activities": "Upcoming activity"},
        {"club_name": "Robotics", "club_description": "Robotics enthusiasts and competitions club", "club_upcoming_activities": "Upcoming activity"},
    ]

    # Insert Clubs
    for club_data in clubs:
        if not db.query(Club).filter_by(club_name=club_data["club_name"]).first():
            db.add(Club(**club_data))
    db.commit()

    clubQuery = db.query(Club).all()
    # Create club requests
    for _ in range(10):
        club_request = ClubRequest(
            clubreq_name=faker.name(),
            clubreq_email=faker.email(),
            clubreq_date=faker.date_time_this_year(),
            club_id=random.choice(clubQuery).id
        )
        db.add(club_request)
    db.commit()

    # Create image requests
    for _ in range(15):
        image_request = ImageRequest(
            imgreq_name=faker.name(),
            imgreq_email=faker.email(),
            imgreq_message=faker.text(),
            imgreq_link=random.choice(images).image_link,
            imgreq_startdate=faker.date_time_this_year(),
            imgreq_enddate=faker.date_time_this_year()
        )
        db.add(image_request)
    db.commit()

    # create schedule types
    schedule_types = [
        {"scheduletype_name": "Availability", "scheduletype_description": "Indicates availability for rooms or tutors."},
        {"scheduletype_name": "Booking", "scheduletype_description": "Indicates a booking event."},
        {"scheduletype_name": "Request", "scheduletype_description": "Indicates a time request awaiting approval."},
    ]

    # Insert ScheduleTypes
    for schedule_type_data in schedule_types:
        if not db.query(ScheduleType).filter_by(scheduletype_name=schedule_type_data["scheduletype_name"]).first():
            db.add(ScheduleType(**schedule_type_data))
    db.commit()

    # create repeat rules
    repeat_rules = [
        {"repeatrule_name": "None", "repeatrule_description": "No repetition"},
        {"repeatrule_name": "Daily", "repeatrule_description": "Repeats daily"},
        {"repeatrule_name": "Weekly", "repeatrule_description": "Repeats weekly"},
        {"repeatrule_name": "Bi_weekly", "repeatrule_description": "Repeats every two weeks."},
        {"repeatrule_name": "Monthly", "repeatrule_description": "Repeats monthly on the same date."},
        {"repeatrule_name": "Yearly", "repeatrule_description": "Repeats yearly on the same date."}
    ]

    # Insert RepeatRules
    for repeat_rule_data in repeat_rules:
        if not db.query(RepeatRule).filter_by(repeatrule_name=repeat_rule_data["repeatrule_name"]).first():
            db.add(RepeatRule(**repeat_rule_data))
    db.commit()

    # Fetch schedule types and repeat rules
    availability_type = db.query(ScheduleType).filter_by(scheduletype_name="Availability").first()
    booking_type = db.query(ScheduleType).filter_by(scheduletype_name="Booking").first()
    repeat_rules_list = db.query(RepeatRule).all()

    # create schedules
    schedules = [
        Schedule(
            schedule_name="Schedule " + str(i),
            schedule_start_time=faker.date_time_this_month(),
            schedule_end_time=faker.date_time_this_month() + timedelta(hours=random.randint(1, 4)),
            schedule_scheduletype_id=random.choice([availability_type.id, booking_type.id]),
            schedule_repeatrule_id=random.choice(repeat_rules_list).id
        )
        for i in range(1, 20)  # Generate 20 schedules
    ]

    for schedule in schedules:
        db.add(schedule)
    db.commit()

    # Fetch schedules
    all_schedules = db.query(Schedule).all()
    users_list = db.query(User).all()
    rooms_list = db.query(Room).all()

    # Create booking rooms
    booking_rooms = [
        BookingRoom(
            bookingroom_number=random.choice(rooms_list).room_number,
            bookingroom_schedule_id=random.choice(all_schedules).id,
            bookingroom_userid=random.choice(users_list).id
        )
        for _ in range(15)  # Generate 15 booking-room entries
    ]

    for booking_room in booking_rooms:
        db.add(booking_room)
    db.commit()

    # create availability rooms
    availability_rooms = [
        AvailabilityRoom(
            availability_room_number=random.choice(rooms_list).room_number,
            availability_room_schedule_id=random.choice(all_schedules).id
        )
        for _ in range(15)  # Generate 15 availability-room entries
    ]
    for availability_room in availability_rooms:
        db.add(availability_room)
    db.commit()

    # create availability tutor
    availability_tutors = []
    used_tutor_ids = set()
    tutorQuery = db.query(User).filter(User.user_roles.any(role_name="Tutor")).all()

    while len(availability_tutors) < len(tutorQuery):
        schedule = random.choice(all_schedules)
        tutor = random.choice(tutorQuery)

        # Skip if tutor id is already used
        if tutor.id in used_tutor_ids:
            continue

        availability_tutors.append(
            AvailabilityTutor(
                availabilitytutor_schedule_id=schedule.id,
                availabilitytutor_tutorid=tutor.id
            )
        )
        used_tutor_ids.add(tutor.id)

    # Add to database
    for availability_tutor in availability_tutors:
        db.add(availability_tutor)

    db.commit()


    # create booking tutors
    booking_tutors = []
    used_tutor_ids = set()
    studentQuery = db.query(User).filter(User.user_roles.any(role_name="Student")).all()

    while len(booking_tutors) < len(tutorQuery):
        schedule = random.choice(all_schedules)
        tutor = random.choice(tutorQuery)
        student = random.choice(studentQuery)

        # Skip if tutor id is already used
        if tutor.id in used_tutor_ids:
            continue

        booking_tutors.append(
            BookingTutor(
                bookingtutor_schedule_id=schedule.id,
                bookingtutor_tutorid=tutor.id,
                bookingtutor_studentid=student.id
            )
        )
        used_tutor_ids.add(tutor.id)

    # Add to database
    for booking_tutor in booking_tutors:
        db.add(booking_tutor)

    db.commit()
