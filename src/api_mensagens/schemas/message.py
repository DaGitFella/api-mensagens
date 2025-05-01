from pydantic import BaseModel
from typing import Union

class MessageCreate(BaseModel):
    id: Union[int, None]
    content: str