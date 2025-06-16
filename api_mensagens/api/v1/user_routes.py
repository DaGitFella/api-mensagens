from http import HTTPStatus
from sqlite3 import IntegrityError

from fastapi import APIRouter
from sqlalchemy import select

from api_mensagens.models.user import User
from api_mensagens.schemas.user import UserPublic, UserCreate, UserUpdate
from api_mensagens.core.security import Session, get_password_hash, CurrentUser
from api_mensagens.core.exceptions import conflict_exception, login_exception

router = APIRouter()


@router.post("", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate, session: Session):
    db_user = session.scalar(select(User).where(User.email == user.email))

    if db_user:
        raise conflict_exception

    hashed_password = get_password_hash(user.password)

    db_user = User(username=user.username, password=hashed_password, email=user.email)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get("/me", response_model=UserPublic)
def get_me(session: Session, current_user: CurrentUser):
    db_user = session.scalar(select(User).where(User.email == current_user.email))

    if not db_user:
        raise login_exception

    return db_user


@router.put("/me", response_model=UserPublic)
def update_me(
    user: UserUpdate,
    session: Session,
    current_user: CurrentUser,
):
    try:
        current_user.username = user.username
        current_user.email = user.email
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise conflict_exception


@router.delete("/me")
def delete_me(
    session: Session,
    current_user: CurrentUser,
):
    session.delete(current_user)
    session.commit()

    return {"message": "Your user has been deleted"}
