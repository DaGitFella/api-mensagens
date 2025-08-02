from fastapi import Body
from api_mensagens.core.security import (
    OAuth2Form,
    verify_password,
    create_access_token,
    Session,
    verify_token,
    create_refresh_token,
)
from api_mensagens.core.exceptions import (
    credentials_exception,
    forbidden_exception,
)
from api_mensagens.models.user import User
from sqlalchemy import select


def login_for_access_token_service(form_data: OAuth2Form, session: Session):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise credentials_exception(detail="Incorrect email or password")

    if not verify_password(form_data.password, user.password):
        raise credentials_exception(detail="Incorrect email or password")

    access_token = create_access_token(
        data={"sub": user.email, "is_staff": user.is_staff}
    )

    refresh_token = create_refresh_token(
        data={"sub": user.email, "is_staff": user.is_staff}
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


def refresh_token_service(refresh_token: str = Body(..., embed=True)):
    payload = verify_token(refresh_token, token_type="refresh")
    user_mail = payload.get("sub")
    is_staff = payload.get("is_staff")

    if not user_mail:
        raise forbidden_exception(detail="Token é inválido")

    new_access_token = create_access_token(
        data={"sub": user_mail, "is_staff": is_staff}
    )

    return {"access_token": new_access_token, "token_type": "bearer"}
