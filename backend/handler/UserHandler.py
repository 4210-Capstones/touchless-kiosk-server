"""
The functions, which the User Controller calls are defined here.
"""
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.classes.db_classes import User
from backend.classes.schemas import UserSchema
from backend.database.Service import UserService
from backend.handler import LoginHandler


def create_user(user: UserSchema, db: Session) -> None:
    """
    Create a user, raise HTTPException if exists.
    """

    user = User(**user.model_dump())  # cast user from UserSchema to UserDB

    user.user_email = user.user_email.lower()     # make email lower case
    user.user_password = LoginHandler.encode_password(user.user_password)  # hash password

    try:
        UserService.create(user, db)
    except IntegrityError:
        raise HTTPException(409, f"A user with the mail {user.user_email} already exists. Try different email.")




def delete_user(user_id: int, db: Session) -> None:
    """
    Deletes a user from the database by their ID. 

   
    """
    try:
        UserService.delete(user_id, db)
    except Exception as e:  # This might be too broad; you could handle specific exceptions if needed
        raise HTTPException(status_code=404, detail="User not found")
