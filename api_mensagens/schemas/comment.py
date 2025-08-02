from pydantic import BaseModel, Field, field_validator


class CommentCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=146,
        description="The content of the comment.",
        examples=[
            "Você está usando 'Menina do Job' na sua dungeon?",
            "Posso usar essa música na minha dungeon?",
        ],
    )

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, value: str):
        if not value.strip():
            raise ValueError("Content cannot be blank or only spaces.")
        return value


class CommentUpdate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=146,
        description="Updated content of the comment.",
    )

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, value: str):
        if not value.strip():
            raise ValueError("Content cannot be blank or only spaces.")
        return value


class PublicComment(BaseModel):
    id: int
    content: str
    author_id: int
    message_id: int


class ListComments(BaseModel):
    comments: list[PublicComment]
