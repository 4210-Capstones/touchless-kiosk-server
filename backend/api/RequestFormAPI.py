from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pathlib import Path
import shutil
import uuid

from backend.database.dependency_db import get_db
from backend.classes.db_classes import ImageRequest, Image, ImageTag, Tag
from backend.classes.schemas import RequestFormSchema

# Define the router
requestform_router = APIRouter(prefix="/imgrequestform", tags=["Request Form"])

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
        unique_filename = f"{uuid.uuid4()}_{image.filename}"
        file_path = upload_dir / unique_filename
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

# Admin Endpoint to View Requests
@requestform_router.get("/imgrequests", response_model=List[RequestFormSchema])
async def get_requests(db: Session = Depends(get_db)):
    """
    Fetch all image requests for admin review.
    """
    requests = db.query(ImageRequest).all()
    if not requests:
        return []
    # Include related tags in the response
    return [
        {
            "imgreq_name": req.imgreq_name,
            "imgreq_email": req.imgreq_email,
            "imgreq_message": req.imgreq_message,
            "imgreq_startdate": req.imgreq_startdate,
            "imgreq_enddate": req.imgreq_enddate,
            "imgreq_tags": [
                {"tag_name": tag.tag_name}
                for tag in db.query(Tag)
                .join(ImageTag)
                .filter(ImageTag.image_link == req.imgreq_link)
                .all()
            ],
            "imgreq_link": req.imgreq_link,
        }
        for req in requests
    ]

# Admin Endpoint to Approve Request
@requestform_router.post("/admin/requests/{request_id}/approve")
async def approve_request(request_id: int, db: Session = Depends(get_db)):
    """
    Approve a specific image request.
    """
    request = db.query(ImageRequest).filter(ImageRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found.")
    # Example approval logic
    request.imgreq_message += " (Approved)"
    db.commit()
    return {"message": f"Request {request_id} approved."}

# Admin Endpoint to Reject Request
@requestform_router.post("/admin/requests/{request_id}/reject")
async def reject_request(request_id: int, db: Session = Depends(get_db)):
    """
    Reject a specific image request and remove its associated data.
    """
    request = db.query(ImageRequest).filter(ImageRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found.")
    
    # Retrieve and delete associated images from the filesystem
    if request.imgreq_link:
        image_path = Path(request.imgreq_link)  # Path to the image
        if image_path.exists():
            try:
                image_path.unlink()  # Delete the image file
                print(f"Deleted image file: {image_path}")
            except Exception as e:
                print(f"Failed to delete image file {image_path}: {e}")

    # Remove the request record from the database
    db.delete(request)
    db.commit()

    return {"message": f"Request {request_id} rejected and removed."}