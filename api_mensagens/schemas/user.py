from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserPublic(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: str = Field(examples=["ADMIN"])


# noinspection PyNestedDecorators
class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str = Field(..., min_length=6, examples=["Ast4!._666"])
    perfil: Optional[str] = "USUARIO"

    # @field_validator("senha", mode="plain")
    # @classmethod
    # def check_password(cls, value: str):
    #     patterns = {
    #         "uppercase letter": r"[A-Z]",
    #         "lowercase letter": r"[a-z]",
    #         "digit": r"\d",
    #         "special character": r"[^a-zA-Z0-9]",
    #     }
    #
    #     missing = [
    #         name
    #         for name, pattern in patterns.items()
    #         if not re.search(pattern, value)
    #     ]
    #
    #     if missing:
    #         raise ValueError(
    #             "Your password must contain a uppercase letter, lowercase letter, digit, special character and be at least 8 characters long."
    #         )
    #     return value


class UserUpdate(BaseModel):
    nome: Optional[str] = Field(
        default=None,
    )
    email: Optional[EmailStr] = Field(
        default=None,
    )
