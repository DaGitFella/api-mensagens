from sqlalchemy.exc import IntegrityError

from sqlalchemy import select
from sqlalchemy.sql.functions import current_user

from api_mensagens.models.user import User
from api_mensagens.schemas.user import UserCreate, UserUpdate
from api_mensagens.core.security import Session, get_password_hash, CurrentUser
from api_mensagens.core.exceptions import conflict_exception


def get_all_users_service(session: Session):
    if (current_user.is_staff)


def create_user_service(user: UserCreate, session: Session):
    db_user = session.scalar(select(User).where(User.email == user.email))
    if db_user:
        raise conflict_exception

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        password=hashed_password,
        email=user.email,
        role='user',
        messages=[],
        comments=[],
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
        current_user.username = user.username
        current_user.email = user.email
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise conflict_exception


def delete_me_service(
    session: Session,
    current_user: CurrentUser,
):
    session.delete(current_user)
    session.commit()

    return {"message": "Your user has been deleted"}
