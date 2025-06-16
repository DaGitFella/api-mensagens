from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from api_mensagens.core.security import Session, verify_password, create_access_token
from api_mensagens.models.user import User
from api_mensagens.schemas.token import Token
from sqlalchemy import select
from api_mensagens.core.exceptions import login_exception, login_exception_password

router = APIRouter()
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2Form, session: Session):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise login_exception

    if not verify_password(form_data.password, user.password):
        raise login_exception_password

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
