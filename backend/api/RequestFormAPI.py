from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pathlib import Path
import shutil

from backend.database.dependency_db import get_db
from backend.classes.db_classes import ImageRequest, Image, ImageTag, Tag

# Define the router
requestform_router = APIRouter(prefix="/imgrequestform", tags=["Form Requests"])

@requestform_router.post("/")
async def handle_form_submission(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    start_date: datetime = Form(...),
    end_date: datetime = Form(...),
    tags: List[str] = Form(...),
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Handle form submissions, save details to the database, and upload images.
    """
    # Validate dates
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date.")
    
    if not tags:
        raise HTTPException(status_code=400, detail="At least one tag must be selected.")

    # Directory to save uploaded images
    upload_dir = Path("uploads/img_requests")
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Save images and track their database records
    uploaded_images = []
    for image in images:
        # Save image file to static/uploads directory
        file_path = upload_dir / image.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            print(f"Saved image to {file_path}")

        # Save image record to the database
        new_image = Image(
            image_link=str(file_path),
            image_confirmed=False
        )
        db.add(new_image)
        db.commit()  # Commit to generate the primary key
        uploaded_images.append(new_image)

    # Save the image request to the database
    new_request = ImageRequest(
        imgreq_name=name,
        imgreq_email=email,
        imgreq_message=message,
        imgreq_startdate=start_date,
        imgreq_enddate=end_date,
        imgreq_link=uploaded_images[0].image_link if uploaded_images else None
    )
    db.add(new_request)
    db.commit()

    # Link tags to the images
    for tag_name in tags:
        tag = db.query(Tag).filter(Tag.tag_name == tag_name).first()
        if not tag:
            continue  # Skip unknown tags
        for uploaded_image in uploaded_images:
            image_tag = ImageTag(
                image_link=uploaded_image.image_link,
                tag_id=tag.id
            )
            db.add(image_tag)
    db.commit()

    return {"message": "Form submitted successfully!"}