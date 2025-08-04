from sqlalchemy.exc import IntegrityError

from sqlalchemy import select

from api_mensagens.models.user import User
from api_mensagens.schemas.user import UserCreate, UserUpdate
from api_mensagens.core.security import Session, get_password_hash, CurrentUser
from api_mensagens.core.exceptions import (
    conflict_exception,
    get_or_404,
    forbidden_exception,
)


def create_user_service(user: UserCreate, session: Session):
    db_user: User = session.scalar(select(User).where(User.email == user.email))

    if db_user:
        raise conflict_exception(detail="User already exists")

    hashed_password = get_password_hash(user.senha)

    db_user = User(
        nome=user.nome,
        senha=hashed_password,
        email=user.email,
        mensagens=[],
        comentarios=[],
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def update_me_service(
    user: UserUpdate,
    session: Session,
    current_user: CurrentUser,
):
    try:
        if user.nome:
            current_user.nome = user.nome

        if user.email:
            current_user.email = user.email

        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise conflict_exception(detail="Email already registered")


def delete_me_service(
    session: Session,
    current_user: CurrentUser,
):
    session.delete(current_user)
    session.commit()

    return {"message": "Your user has been deleted"}


def delete_user_service(
    session: Session, current_user: CurrentUser, user_id: int
):
    if current_user.perfil == 'admin' or current_user.id == user_id:
        user = get_or_404(session, User, user_id)
        session.delete(user)
        session.commit()
        return {"message": "User has been deleted"}

    raise forbidden_exception("You can't delete other users.")


def update_user_service(
    session: Session,
    update_data: UserUpdate,
    current_user: CurrentUser,
    user_id: int,
):
    if current_user.perfil == 'admin' or current_user.id != user_id:
        raise forbidden_exception("You can't update other users.")

    if update_data.username:
        current_user.username = update_data.username

    if update_data.email:
        current_user.email = update_data.email

    session.commit()
    session.refresh(current_user)
    return current_user
