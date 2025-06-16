from pydantic import BaseModel, Field, field_validator


class MessageCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=146,
        description="The content of the message.",
        examples=["Baesse heróico", "Vincente não me deu 100 :/"],
    )

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, value: str):
        if not value.strip():
            raise ValueError(
                "Content cannot be blank or only spaces"
            )  # pragma: no cover
        return value


class PublicMessage(BaseModel):
    id: int
    content: str


class ListMessages(BaseModel):
    messages: list[PublicMessage]
