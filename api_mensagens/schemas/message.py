from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from api_mensagens.schemas.comment import PublicComment


class MessageCreate(BaseModel):
    titulo: str = Field(
        min_length=1,
        max_length=100,
        description="Título da mensagem",
        examples=["A odisséia de Baesse"],
    )
    conteudo: str = Field(
        min_length=1,
        max_length=146,
        description="The content of the message.",
        examples=["Baesse heróico", "Vincente não me deu 100 :/"],
    )

    @field_validator("conteudo", "titulo")
    @classmethod
    def content_not_blank(cls, value: str):
        if not value.strip():
            raise ValueError(
                "Content cannot be blank or only spaces"
            )  # pragma: no cover
        return value


class MessagePatch(BaseModel):
    titulo: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Título da mensagem",
        examples=["A odisséia de Baesse"],
    )
    conteudo: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=146,
        description="The content of the message.",
        examples=["Baesse heróico", "Vincente não me deu 100 :/"],
    )

    @field_validator("conteudo", "titulo")
    @classmethod
    def content_not_blank(cls, value: str):
        if not value.strip():
            raise ValueError(
                "Content cannot be blank or only spaces"
            )  # pragma: no cover
        return value


class PublicMessage(BaseModel):
    id: int
    titulo: str
    conteudo: str
    usuario_id: int
    data_criacao: datetime


class PrivateMessage(BaseModel):
    id: int
    titulo: str
    conteudo: str
    usuario_id: int
    comentarios: list[PublicComment]


class ListMessages(BaseModel):
    mensagens: list[PrivateMessage]


class ListPublicMessages(BaseModel):
    mensagens: list[PublicMessage]
