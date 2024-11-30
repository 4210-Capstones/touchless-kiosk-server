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
    try:
        # Validate input
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date cannot be after end date.")
        if not tags:
            raise HTTPException(status_code=400, detail="At least one tag must be selected.")

        # Save images
        upload_dir = Path("uploads/img_requests")
        upload_dir.mkdir(parents=True, exist_ok=True)

        uploaded_images = []
        for image in images:
            unique_filename = f"{uuid.uuid4()}_{image.filename}"
            file_path = upload_dir / unique_filename
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            new_image = Image(image_link=str(file_path), image_confirmed=False)
            db.add(new_image)
            db.commit()
            uploaded_images.append(new_image)

        # Save the image request
        new_request = ImageRequest(
            imgreq_name=name,
            imgreq_email=email,
            imgreq_message=message,
            imgreq_startdate=start_date,
            imgreq_enddate=end_date,
            imgreq_link=uploaded_images[0].image_link if uploaded_images else None,
        )
        db.add(new_request)
        db.commit()

        # Link tags to the images
        for tag_name in tags:
            tag = db.query(Tag).filter(Tag.tag_name == tag_name).first()
            if tag:
                for uploaded_image in uploaded_images:
                    image_tag = ImageTag(image_link=uploaded_image.image_link, tag_id=tag.id)
                    db.add(image_tag)
        db.commit()

        # Return a response including the new request's ID
        return {"message": "Form submitted successfully!", "id": new_request.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Admin Endpoint to View Requests
@requestform_router.get("/imgrequests", response_model=List[RequestFormSchema])
async def get_requests(db: Session = Depends(get_db)):
    """
    Fetch all image requests for admin review.
    """
    requests = db.query(ImageRequest).all()
    if not requests:
        return []

    return [
        {
            "id": req.id,  # Ensure that the ID is included here
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
            "imgreq_link": f"/uploads/img_requests/{Path(req.imgreq_link).name}" if req.imgreq_link else None,
        }
        for req in requests
    ]


# Admin Endpoint to Approve Request
@requestform_router.post("/admin/requests/{request_id}/approve")
async def approve_request(request_id: int, db: Session = Depends(get_db)):
    """
    Approve a specific image request, move image to the slideshow folder, and update metadata.
    """
    request = db.query(ImageRequest).filter(ImageRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found.")
    
    # Define source and destination
    if not request.imgreq_link:
        raise HTTPException(status_code=400, detail="Request has no associated image.")
    source = Path(request.imgreq_link)  # Points to server/uploads/img_requests
    destination_folder = Path("../../front-end/images").resolve()
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination = destination_folder / source.name
    
    try:
        # Move image to the slideshow folder
        shutil.move(str(source), str(destination))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to move image: {e}")
    
    # Update metadata (assume metadata file path is defined)
    metadata_file = "uploads/slideshow_metadata.json"
    initialize_metadata_file(metadata_file)
    with open(metadata_file, "r") as file:
        metadata = json.load(file)
    metadata[destination.name] = (datetime.date.today() + datetime.timedelta(days=7)).isoformat()
    with open(metadata_file, "w") as file:
        json.dump(metadata, file, indent=4)
    
    # Mark request as approved
    request.imgreq_message += " (Approved)"
    db.commit()
    return {"message": f"Request {request_id} approved."}

# Admin Endpoint to Reject Request
@requestform_router.post("/admin/requests/{request_id}/reject")
async def reject_request(request_id: int, db: Session = Depends(get_db)):
    """
    Reject a specific image request and delete its associated data.
    """
    request = db.query(ImageRequest).filter(ImageRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found.")
    
    # Remove associated image
    if request.imgreq_link:
        image_path = Path(request.imgreq_link)
        if image_path.exists():
            try:
                image_path.unlink()  # Delete the image file
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to delete image: {e}")
    
    # Remove request record
    db.delete(request)
    db.commit()
    return {"message": f"Request {request_id} rejected and removed."}