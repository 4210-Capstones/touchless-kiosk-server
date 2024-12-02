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

class TagSchema(BaseModel):
    tag_name: str
    tag_description: Optional[str] = None

    class Config:
        orm_mode = True

class RequestFormSchema(BaseModel):
    id: int
    imgreq_name: str = Field(..., example="John Doe")
    imgreq_email: EmailStr = Field(..., example="jdoe@uno.edu")
    imgreq_message: str = Field(..., example="Requesting this image to be displayed all of next week")
    imgreq_startdate: datetime = Field(..., example="2024-12-02T00:00:00")
    imgreq_enddate: datetime = Field(..., example="2024-12-06T23:59:59")
    imgreq_tags: List[TagSchema] = Field(..., example=[{"tag_name": "acm"}])
    imgreq_links: Optional[List[str]] = Field(None, example=["/uploads/img_requests/jdoe_request_1/image_123.png"])

    class Config:
        from_attributes = True