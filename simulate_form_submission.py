import requests
from datetime import datetime, timedelta
from pathlib import Path
import random
import mimetypes
import os

# Environment Variables for API URL
API_URL = os.getenv("API_URL", "http://localhost:8000/imgrequestform/")

# Path to test images
TEST_IMAGE_DIR = Path("tests/test_images")
TEST_IMAGES = [
    "test0.jpg",
    "test1.jpg",
    "test2.png",
    "test3.png",
    "test4.png",
    "test5.jpg",
    "test6.jpg",
    "test7.jpg",
    "test8.jpg",
]

# Random Tags
TAGS = ["Hackathon", "ACM", "ACMW", "CTF", "GDSC", "ICPC", "IEEE", "IGDA", "Robotics", "WebDev", "Workshops", "Jobs", "Research"]

def get_mime_type(file_path):
    """
    Get the MIME type of a file.
    """
    return mimetypes.guess_type(file_path)[0] or "application/octet-stream"

def simulate_form_submission():
    """
    Simulate a form submission to the `/imgrequestform/` endpoint.
    """
    # Prepare form data
    form_data = {
        "name": "Test User",
        "email": "testuser@uno.edu",
        "message": "This is a test message for form submission.",
        "start_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "end_date": (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%dT%H:%M:%S"),
        "tags": random.sample(TAGS, random.randint(1, 5)),
    }

    image_files = [
        ("images", (image, open(TEST_IMAGE_DIR / image, "rb"), get_mime_type(TEST_IMAGE_DIR / image)))
        for image in random.sample(TEST_IMAGES, random.randint(1, 3))
        if (TEST_IMAGE_DIR / image).exists()
    ]

    if not image_files:
        print("No valid images found in the test directory.")
        return

    try:
        response = requests.post(API_URL, data=form_data, files=image_files)
        if response.status_code == 200:
            print("Form submission successful:", response.json())
        else:
            print(f"Form submission failed with status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        for _, file_tuple in image_files:
            file_tuple[1].close()

if __name__ == "__main__":
    simulate_form_submission()
