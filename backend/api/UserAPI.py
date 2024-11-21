"""
User endpoints will be defined here.
Therefore, a separate router is created. It has the prefix "/users"
All endpoints which are wrapped with this router will start with "/users".
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from classes.db_classes import User
from classes.responses import UserResponse
from classes.schemas import UserSchema
from database.dependency_db import get_db
from handler import UserHandler
from handler.LoginHandler import get_current_user

user_router = APIRouter(prefix="/users", tags=["Users"])    # tags define metadata for documentation purposes

@user_router.post("/", status_code=201)
async def create_user(user: UserSchema, db: Session = Depends(get_db)) -> None:
    """
    An endpoint to create a new user.
    """

    return UserHandler.create_user(user, db)


"""
Multiple "advanced" stuff is happening here.

First of all, the user is automatically retrieved via Depends. Depends is essentially a function, which FastAPI will
automatically execute if the endpoint is accessed. 
If the user has logged in, they will receive a token. This token must be send in the header of the request in the form of:
{"Authorization": f'Bearer {access_token}'}
OpenAPI Docs will do that for you. 
The token contains user information, with witch the user will be retrieved with.
The endpoint is restricted, a "Not Authenticated" exception will be raised if the token is not provided, invalid or expired.

Second, we can see some FastAPI "magic" here:
user is of type UserDB, which is also indicated in the return type. Otherwise we would get a warning and "confuse" the 
IDE, so that it would eventually provide wrong code completion information.
However, UserDB contains the hashed password, which we should not return. Therefore, we defined a separate UserResponse
class. It is indicated as response_model in the endpoint wrapper. With that, FastAPI will automatically cast the user 
from type UserDB to UserResponse, removing the password in the response.

A "classical" approach is commented out below (calls a commented function in handler). 
"""
@user_router.get("/profile", status_code=200, response_model=UserResponse)
async def get_user(user: User = Depends(get_current_user)) -> User:
    """
    Returns the user's profile information. User parameter is automatically resolved. User must be authenticated.
    """

    return user