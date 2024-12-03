from sqlalchemy.orm import Session
from backend.database.Service import TutoringService
from backend.classes.db_classes import Tutoring
from fastapi import HTTPException
from datetime import time


def add_tutor(name: str, email: str, time_in: time, time_out: time, db: Session) -> None:
    """Add a new tutor to the database."""
    tutor = Tutoring(name=name, email=email, time_in=time_in, time_out=time_out)
    try:
        TutoringService.create(tutor, db)
        print(f"Tutor {tutor.name} added successfully")
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"An error occurred adding a tutor: {error}")

def get_tutors(db: Session) -> List[Tutoring]:
    """Retrieve all tutors from the database."""
    return TutoringService.get_all(db)

def update_tutor(tutor_id: int, name: str = None, email: str = None, time_in: time = None, time_out: time = None):
    """Update a tutor's details."""
    tutor = TutoringService.get(tutor_id, db)
    if not tutor:
        print(f"Tutor with ID {tutor_id} not found.")

    if name:
        tutor.name = name
    if email:
        tutor.email = email
    if time_in:
        tutor.time_in = time_in
    if time_out:
        tutor.time_out = time_out
    
    TutoringService.update(tutor_id, tutor, db)
    print(f"Tutor ID {tutor_id} updated successfully.")

def delete_tutor(tutor_id: int, db: Session) -> None:
    """Delete a tutor from the database."""
    try:
        TutoringService.delete(tutor_id, db)
        print(f"Tutor ID {tutor_id} deleted successfully.")
    except Exception as error:
        raise HTTPException(status_code=404, detail=f"An error occurred deleting tutor {tutor_id}: {error} ")