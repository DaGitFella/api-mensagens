from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("password")
    def strip_whitespace(cls, value: str) -> str:
        return value.strip()
