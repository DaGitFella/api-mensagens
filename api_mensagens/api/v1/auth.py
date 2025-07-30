from fastapi import APIRouter, Body
from api_mensagens.core.security import Session, OAuth2Form
from api_mensagens.schemas.token import Token, AccessToken
from api_mensagens.services.auth_service import (
    login_for_access_token_service,
    refresh_token_service,
)

router = APIRouter()


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2Form, session: Session):
    return login_for_access_token_service(form_data, session)


@router.post("/refresh", response_model=AccessToken)
def get_refresh_token(refresh_token: str = Body(..., embed=True)):
    return refresh_token_service(refresh_token)
