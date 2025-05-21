from pydantic import BaseModel, ConfigDict


class MessageCreate(BaseModel):
    content: str

class PublicMessage(BaseModel):
    id: int
    content: str

class ListMessages(BaseModel):
    messages: list[PublicMessage]