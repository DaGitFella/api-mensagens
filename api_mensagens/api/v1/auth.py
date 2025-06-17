from fastapi import APIRouter
from api_mensagens.core.security import Session, OAuth2Form
from api_mensagens.schemas.token import Token
from api_mensagens.services.auth_service import login_for_access_token_service

router = APIRouter()


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2Form, session: Session):
    return login_for_access_token_service(form_data, session)
