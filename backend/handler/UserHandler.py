"""
The functions, which the User Controller calls are defined here.
"""
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from classes.db_classes import User
from classes.schemas import UserSchema
from database.Service import UserService
from handler import LoginHandler


def create_user(user: UserSchema, db: Session) -> None:
    """
    Create a user, raise HTTPException if exists.
    """

    user = User(**user.model_dump())  # cast user from UserSchema to UserDB

    user.email = user.email.lower()     # make email lower case
    user.password = LoginHandler.encode_password(user.password)  # hash password

    try:
        UserService.create(user, db)
    except IntegrityError:
        raise HTTPException(409, f"A user with the mail {user.email} already exists. Try different email.")