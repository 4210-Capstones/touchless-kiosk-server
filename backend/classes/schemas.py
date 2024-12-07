"""
Schemas are used as input to the API
"""

from pydantic import EmailStr, Field
from pydantic import BaseModel


class UserSchema(BaseModel):
    user_email: EmailStr
    user_password: str =  Field(min_length=8, description="Password must be at least 8 characters long")