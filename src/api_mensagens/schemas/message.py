from pydantic import BaseModel
from typing import Union

class MessageCreate(BaseModel):
    id: int = None
    content: str