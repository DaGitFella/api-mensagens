from typing import Annotated

import jwt
from fastapi import Depends
from sqlalchemy.orm import Session
from api_mensagens.db.session import get_session
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import DecodeError, encode, PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from api_mensagens.models.user import User
from api_mensagens.core.config import settings
from api_mensagens.core.exceptions import credentials_exception, forbidden_exception

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

Session = Annotated[Session, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]

def verify_token(token: str, token_type: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != token_type:
            raise PyJWTError()
        return payload
    except PyJWTError:
        raise forbidden_exception(
            detail='token inválido ou inspirado'
        )

def get_current_user(session: Session, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_email = payload.get("sub")

        if not subject_email:
            raise credentials_exception(detail="Invalid email or password")

    except DecodeError:
        raise credentials_exception()

    user = session.scalar(select(User).where(User.email == subject_email))

    if not user:
        raise credentials_exception(detail="Invalid email or password")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

def require_role(*roles: list[str]):
    def role_checker(user = Depends(get_current_user)):
        if user.role not in roles:
            raise forbidden_exception(detail="Você não tem permissão para acessar esse recurso")
        return user
    return role_checker

adminRequired = Annotated[User, Depends(require_role("admin"))]

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        days=settings.ACCESS_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({"exp": expire})
    encoded_jwt = encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt

