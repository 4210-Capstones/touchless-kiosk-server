from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    email: EmailStr