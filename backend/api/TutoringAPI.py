from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.dependency_db import get_db
from backend.handler import TutoringHandler
from datetime import time

tutoring_router = APIRouter(prefix="/tutors", tags=["Tutoring"])

@tutoring_router.post("/", status_code=201)
async def add_tutor(name: str, email: str, time_in: time, time_out: time, db: Session = Depends(get_db)):
    """API endpoint to add a tutor"""
    TutoringHandler.add_tutor(name, email, time_in, time_out, db)

@tutoring_router.get("/", status_code=200)
async def get_tutors(db: Session = Depends(get_db)):
    """API endpoint to get all tutors"""
    return TutoringHandler.get_tutors(db)

@tutoring_router.put("/{tutor_id}", status_code=200)
async def update_tutor(tutor_id: int, name: str = None, email: str = None, time_in: time = None, time_out: time = None, db: Session = Depends(get_db)):
    """API endpoint to update a tutor"""
    TutoringHandler.update_tutor(tutor_id, name, email, time_in, time_out, db)

@tutoring_router.delete("/{tutor_id}", status_code=204)
async def delete_tutor(tutor_id: int, db: Session = Depends(get_db)):
    """API endpoint to delete a tutor"""
    TutoringHandler.delete_tutor(tutor_id, db)