from api_mensagens.core.security import (
    OAuth2Form,
    verify_password,
    create_access_token,
    Session,
)
from api_mensagens.core.exceptions import login_exception, login_exception_password
from api_mensagens.models.user import User
from sqlalchemy import select


def login_for_access_token_service(form_data: OAuth2Form, session: Session):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise login_exception

    if not verify_password(form_data.password, user.password):
        raise login_exception_password

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
