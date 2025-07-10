from api_mensagens.core.security import (
    OAuth2Form,
    verify_password,
    create_access_token,
    Session,
)
from api_mensagens.core.exceptions import credentials_exception
from api_mensagens.models.user import User
from sqlalchemy import select


def login_for_access_token_service(form_data: OAuth2Form, session: Session):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise credentials_exception(detail="Incorrect email or password")

    if not verify_password(form_data.password, user.password):
        raise credentials_exception(detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email, "role": user.role})

    return {"access_token": access_token, "token_type": "bearer"}
