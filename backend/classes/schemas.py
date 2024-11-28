"""
Schemas are used as input to the API
"""

from pydantic import EmailStr, Field
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional



class UserSchema(BaseModel):
    user_email: EmailStr
    user_password: str =  Field(min_length=8, description="Password must be at least 8 characters long")

class RequestFormSchema(BaseModel):
    imgreq_name: str
    imgreq_email: EmailStr
    imgreq_message: str
    imgreq_startdate: datetime
    imgreq_enddate: datetime
    imgreq_tags: List[str]

    class Config:
        orm_mode = True