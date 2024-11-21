"""
If the API needs to send more complicated objects, they will be a Response.
"""

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    email: EmailStr