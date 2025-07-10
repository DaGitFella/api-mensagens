from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime


# noinspection PyNestedDecorators
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8, examples=["Ast4!._666"])

    @field_validator("password", mode="plain")
    @classmethod
    def check_password(cls, value: str):
        patterns = {
            "uppercase letter": r"[A-Z]",
            "lowercase letter": r"[a-z]",
            "digit": r"\d",
            "special character": r"[^a-zA-Z0-9]",
        }

        missing = [
            name
            for name, pattern in patterns.items()
            if not re.search(pattern, value)
        ]

        if missing:
            raise ValueError(
                "Your password must contain a uppercase letter, lowercase letter, digit, special character and be at least 8 characters long."
            )
        return value


class UserUpdate(BaseModel):
    username: str
    email: EmailStr
