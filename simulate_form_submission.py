import requests
from datetime import datetime, timedelta
from pathlib import Path
import random
import mimetypes
import os
from sqlalchemy.orm import Session
from backend.database.config_db import create_db, engine
from backend.classes.db_classes import Tag, Role, User, ImageRequest  # Import all necessary models
from backend.database.dependency_db import get_db  # Import session dependencies

# Environment Variables for API URL
API_URL = os.getenv("API_URL", "http://localhost:8000/imgrequestform/")

# Path to test images
TEST_IMAGE_DIR = Path("tests/test_images")
TEST_IMAGES = {
    "SabrinaFarmer.png": ["ACMW"],
    "rubberducks.png": ["ACMW"],
    "CyberSecurityWeek.png": ["CTF"],
    "ClubMeeting.png": ["IEEE", "ACM", "ACMW"],
    "GameJam.png": ["IGDA"],
    "VideoGameDay.png": ["IGDA"],
    "gamenight.jpg": ["IGDA"],
    "test2.png": ["Research"],
    "test3.png": ["Robotics"],
    "test4.png": ["GDSC", "ICPC"],
}

# Random Tags
TAGS = ["Hackathon", "ACM", "ACMW", "CTF", "GDSC", "ICPC", "IEEE", "IGDA", "Robotics", "WebDev", "Workshops", "Jobs", "Research"]

# Random Names and Emails
NAMES_AND_EMAILS = [
    ("Alice Johnson", "ajohnson@uno.edu"),
    ("Bob Smith", "bsmith@uno.edu"),
    ("Charlie Lee", "clee@uno.edu"),
    ("Diana Prince", "dprince@uno.edu"),
    ("Ethan Hunt", "ehunt@uno.edu"),
    ("Han Solo", "hsolo@uno.edu"),
    ("Gordon Freeman", "gfreeman@uno.edu"),
    ("Alan Turing", "aturing@uno.edu"),
    ("Igor Stravinsky", "istravinsky@uno.edu"),
    ("Jane Doe", "jdoe@uno.edu"),
]

# Random Messages
MESSAGES = [
    "This is a test message for form submission.",
    "Please display this image during our event next week.",
    "I am requesting this image for our club's promotional activities.",
    "This image should be shown during the robotics workshop.",
    "This is an important image for our Hackathon promotion.",
    "The picture should be included in next week's slide deck.",
    "This submission is part of the research showcase.",
    "Please make sure this image is used during the opening ceremony.",
    "A test image for internal evaluation, please ignore.",
    "Promotional image for the upcoming tech jobs fair.",
]

def get_mime_type(file_path):
    """
    Get the MIME type of a file.
    """
    return mimetypes.guess_type(file_path)[0] or "application/octet-stream"

def setup_database():
    print("[INFO] Setting up the database...")
    """
    Ensures that the necessary tables are created in the database.
    """
    # Create the database and tables if they do not exist
    create_db()

    # Add initial mock data like tags, roles, etc. if needed
    session = Session(bind=engine)

    # Check if tags already exist in the database, if not, create them
    if not session.query(Tag).first():
        print("[INFO] Adding initial tags to the database...")
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
        session.add_all(tags)
        session.commit()
        print("[INFO] Initial tags added successfully.")
    else:
        print("[INFO] Tags already exist in the database. Skipping initial setup.")
    session.close()

def simulate_form_submission():
    print("[INFO] Simulating form submission...")
    """
    Simulate a form submission to the `/imgrequestform/` endpoint.
    """
    # Setup the database first
    setup_database()

    # Choose random name, email, and message
    print("[INFO] Selecting random name, email, and message...")
    name, email = random.choice(NAMES_AND_EMAILS)
    message = random.choice(MESSAGES)

    # Choose random images and their associated tags
    print("[INFO] Selecting random images...")
    selected_images = random.sample(list(TEST_IMAGES.items()), random.randint(1, 3))
    image_files = []
    selected_tags = set()  # Using a set to avoid duplicate tags

    for image_name, associated_tags in selected_images:
        image_path = TEST_IMAGE_DIR / image_name
        if image_path.exists():
            print(f"[INFO] Adding image: {image_name}")
            image_files.append(
                ("images", (image_name, open(image_path, "rb"), get_mime_type(image_path)))
            )
            selected_tags.update(associated_tags)  # Add the associated tags for each selected image
        else:
            print(f"[WARNING] Image not found: {image_name}")

    if not image_files:
        print("[ERROR] No valid images found in the test directory. Aborting submission.")
        return

    # Prepare form data
    print("[INFO] Preparing form data...")
    form_data = {
        "name": name,
        "email": email,
        "message": message,
        "start_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "end_date": (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%dT%H:%M:%S"),
        "tags": list(selected_tags),  # Convert the set of tags to a list
    }

    print("[INFO] Form data prepared:")
    print(f"    Name: {name}")
    print(f"    Email: {email}")
    print(f"    Message: {message}")
    print(f"    Tags: {list(selected_tags)}")
    print(f"    Start Date: {form_data['start_date']}")
    print(f"    End Date: {form_data['end_date']}")
    print(f"    Number of Images: {len(image_files)}")

    try:
        # Make the POST request to submit the form
        print("[INFO] Submitting the form to the API...")
        response = requests.post(API_URL, data=form_data, files=image_files)
        if response.status_code == 200:
            print("[SUCCESS] Form submission successful:", response.json())
        else:
            print(f"[ERROR] Form submission failed with status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[EXCEPTION] An error occurred during form submission: {e}")
    finally:
        # Close all opened files
        print("[INFO] Closing all opened image files...")
        for _, file_tuple in image_files:
            print(f"    Closing {file_tuple[0]}")
            file_tuple[1].close()

if __name__ == "__main__":
    simulate_form_submission()
