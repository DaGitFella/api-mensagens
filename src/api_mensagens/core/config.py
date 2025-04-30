from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str


settings = Settings(DATABASE_URL = "sqlite:///./db/api-mensagens.sqlite3", SECRET_KEY = "secret")
