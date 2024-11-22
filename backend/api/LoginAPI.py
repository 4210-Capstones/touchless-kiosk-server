from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.classes.other import Token
from backend.database.dependency_db import get_db
from backend.handler import LoginHandler


login_router = APIRouter(prefix="/login", tags=["Login"])


@login_router.post("/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict[str, str]:
    """
    The endpoint provides a login functionality for users.
    The endpoint expects a form data body (not json) like
    {"username": {user_email}, "password": {password}}

    It returns
    {"access_token": access_token, "token_type": "bearer"}
    """

    return LoginHandler.login_for_access_token(form_data, db)