from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
