from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    refresh_token_type: str = "refresh"


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
