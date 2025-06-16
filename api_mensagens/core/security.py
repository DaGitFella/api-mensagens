from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from api_mensagens.db.session import get_session


session = Annotated[Session, Depends(get_session)]