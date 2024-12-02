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

from fastapi.logger import logger  # Use the default FastAPI logger

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
        print("[INFO] Starting form submission handling...")

        
        # Validate input
        if start_date > end_date:
            print("[ERROR] Start date is after end date.")
            raise HTTPException(status_code=400, detail="Start date cannot be after end date.")
        if not tags:
            print("[ERROR] No tags provided.")
            raise HTTPException(status_code=400, detail="At least one tag must be selected.")

        print("[INFO] Creating new ImageRequest in database...")
        # Save the image request without the imgreq_link first (since the directory is not created yet)
        new_request = ImageRequest(
            imgreq_name=name,
            imgreq_email=email,
            imgreq_message=message,
            imgreq_startdate=start_date,
            imgreq_enddate=end_date,
            imgreq_link=None  # Set to None temporarily
        )
        db.add(new_request)
        db.commit()  # Commit to get request ID
        print(f"[INFO] Created ImageRequest with ID: {new_request.id}")

        # Create a unique directory for this request
        request_dir = Path(f"backend/uploads/img_requests/{email.split('@')[0]}_request_{new_request.id}")
        request_dir.mkdir(parents=True, exist_ok=True)
        print(f"[INFO] Created directory for request: {request_dir}")

        # Save images
        img_links = []
        for image in images:
            unique_filename = f"{uuid.uuid4()}_{image.filename}"
            file_path = request_dir / unique_filename
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            relative_file_path = f"/uploads/img_requests/{email.split('@')[0]}_request_{new_request.id}/{unique_filename}"
            img_links.append(relative_file_path)
            print(f"[INFO] Saved image: {unique_filename} at {relative_file_path}")


        # Update the image request with the list of image links
        new_request.imgreq_link = ','.join(img_links)  # Storing multiple file paths as a comma-separated string
        db.commit()
        print(f"[INFO] Updated ImageRequest ID {new_request.id} with image links.")

        # Link tags to the images (just tag the request for simplicity)
        for tag_name in tags:
            tag = db.query(Tag).filter(Tag.tag_name == tag_name).first()
            if tag:
                # Associate the tag with the request itself (if the tag does not exist, create a new one)
                image_tag = ImageTag(image_link=new_request.imgreq_link, tag_id=tag.id)
                db.add(image_tag)
                print(f"[INFO] Linked tag '{tag_name}' with ImageRequest ID {new_request.id}.")
        db.commit()
        print(f"[INFO] Form submission for ImageRequest ID {new_request.id} completed successfully.")
        # Return a response including the new request's ID
        return {"message": "Form submitted successfully!", "id": new_request.id}

    except HTTPException as e:
        print(f"[ERROR] HTTPException occurred: {e.detail}")
        raise e
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@requestform_router.get("/imgrequests", response_model=List[RequestFormSchema])
async def get_requests(db: Session = Depends(get_db)):
    """
    Fetch all image requests for admin review.
    """
    print("[INFO] Starting to fetch image requests for admin review.")

    # Fetch all requests from the database
    requests = db.query(ImageRequest).all()
    print(f"[INFO] Number of requests fetched: {len(requests)}")

    if not requests:
        print("[INFO] No image requests found in the database.")
        return []

    response_data = []

    for req in requests:
        print(f"[INFO] Processing ImageRequest ID: {req.id}")

        # Collect all tags related to the image request
        tags = db.query(Tag).join(ImageTag).filter(ImageTag.image_link.like(f"%_request_{req.id}%")).all()
        tag_names = [tag.tag_name for tag in tags]
        print(f"[INFO] Tags found for ImageRequest ID {req.id}: {tag_names}")

        # Parse the stored imgreq_link (which contains the comma-separated image file paths)
        img_links = req.imgreq_link.split(',') if req.imgreq_link else []
        print(f"[INFO] Image links found for ImageRequest ID {req.id}: {img_links}")

        # Construct response data for the request
        response_data_item = {
            "id": req.id,
            "imgreq_name": req.imgreq_name,
            "imgreq_email": req.imgreq_email,
            "imgreq_message": req.imgreq_message,
            "imgreq_startdate": req.imgreq_startdate,
            "imgreq_enddate": req.imgreq_enddate,
            "imgreq_tags": [{"tag_name": tag.tag_name} for tag in tags],
            "imgreq_links": img_links,
        }
        response_data.append(response_data_item)
        print(f"[INFO] Response data prepared for ImageRequest ID {req.id}: {response_data_item}")

    print("[INFO] Completed fetching and preparing response for all image requests.")
    return response_data

# Admin Endpoint to Approve Request
@requestform_router.post("/admin/requests/{request_id}/approve")
async def approve_request(request_id: int, db: Session = Depends(get_db)):
    """
    Approve a specific image request, move images to the slideshow folder, and update metadata.
    """
    request = db.query(ImageRequest).filter(ImageRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found.")
    
    # Define source and destination
    if not request.imgreq_link:
        raise HTTPException(status_code=400, detail="Request has no associated images.")
    
    source = Path(request.imgreq_link)  # Directory containing images
    destination_folder = Path("../../../touchless-kiosk-front-end/images").resolve() / f"{request.imgreq_name}_request_{request.id}"
    logger.info(f"Source directory: {source}")
    logger.info(f"Destination directory: {destination_folder}")
    
    # Ensure destination directory exists
    try:
        destination_folder.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create destination directory: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create destination directory: {e}")

    # Iterate over each image file and move it to the destination
    try:
        for image_file in source.iterdir():
            if image_file.is_file():
                destination_path = destination_folder / image_file.name
                logger.info(f"Moving {image_file} to {destination_path}")
                shutil.move(str(image_file), str(destination_path))
                print(f"Moving {image_file} to {destination_path}")
    except Exception as e:
        logger.error(f"Failed to move images: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to move images: {e}")

    # Remove the source directory if it's empty after moving all images
    try:
        if source.exists() and source.is_dir():
            os.rmdir(source)
            logger.info(f"Removed empty source directory: {source}")
    except OSError as e:
        logger.warning(f"Could not remove source directory {source}: {e}")

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
    
    # Remove associated images directory
    if request.imgreq_link:
        images_dir = Path(request.imgreq_link)
        if images_dir.exists() and images_dir.is_dir():
            try:
                shutil.rmtree(images_dir)  # Delete the entire directory and its contents
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to delete images: {e}")

    # Remove request record
    db.delete(request)
    db.commit()
    return {"message": f"Request {request_id} rejected and removed."}