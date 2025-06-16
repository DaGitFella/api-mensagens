from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from api_mensagens.db.session import get_session
from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode,encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from api_mensagens.models.user import User
from api_mensagens.core.config import settings


pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
session = Annotated[Session, Depends(get_session)]

