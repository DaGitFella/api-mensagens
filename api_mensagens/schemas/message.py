from typing import Optional

from pydantic import BaseModel, Field, field_validator
from api_mensagens.schemas.comment import PublicComment


class MessageCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
        description="Título da mensagem",
        examples=["A odisséia de Baesse"],
    )
    content: str = Field(
        min_length=1,
        max_length=146,
        description="The content of the message.",
        examples=["Baesse heróico", "Vincente não me deu 100 :/"],
    )

    @field_validator("content", "title")
    @classmethod
    def content_not_blank(cls, value: str):
        if not value.strip():
            raise ValueError(
                "Content cannot be blank or only spaces"
            )  # pragma: no cover
        return value


class MessagePatch(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Título da mensagem",
        examples=["A odisséia de Baesse"],
    )
    content: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=146,
        description="The content of the message.",
        examples=["Baesse heróico", "Vincente não me deu 100 :/"],
    )

    @field_validator("content", "title")
    @classmethod
    def content_not_blank(cls, value: str):
        if not value.strip():
            raise ValueError(
                "Content cannot be blank or only spaces"
            )  # pragma: no cover
        return value


class PublicMessage(BaseModel):
    id: int
    title: str
    content: str
    user_id: int


class PrivateMessage(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    comments: list[PublicComment]


class ListMessages(BaseModel):
    messages: list[PrivateMessage]


class ListPublicMessages(BaseModel):
    messages: list[PublicMessage]
