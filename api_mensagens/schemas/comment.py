from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class CommentCreate(BaseModel):
    conteudo: str = Field(
        min_length=1,
        max_length=146,
        description="The content of the comment.",
        examples=[
            "Você está usando 'Menina do Job' na sua dungeon?",
            "Posso usar essa música na minha dungeon?",
        ],
    )

    @field_validator("conteudo")
    @classmethod
    def content_not_blank(cls, value: str):
        if not value.strip():
            raise ValueError("Content cannot be blank or only spaces.")
        return value


class CommentUpdate(BaseModel):
    conteudo: str = Field(
        min_length=1,
        max_length=146,
        description="Updated content of the comment.",
    )

    @field_validator("conteudo")
    @classmethod
    def content_not_blank(cls, value: str):
        if not value.strip():
            raise ValueError("Content cannot be blank or only spaces.")
        return value


class PublicComment(BaseModel):
    id: int
    conteudo: str
    usuario_id: int
    mensagem_id: int
    data_criacao: datetime


class ListComments(BaseModel):
    comentarios: list[PublicComment]
