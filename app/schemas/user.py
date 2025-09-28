# make pydantic models for user for api requests

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Base user Scheme
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


# What client needs to send while creating a user
class UserCreate(UserBase):
    password: str


# Reading user info from DB
class UserRead(UserBase):
    id: int
    active: bool
    created_at: datetime
    modified_at: Optional[datetime]

    class Config:
        orm_mode = True


# For login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str
