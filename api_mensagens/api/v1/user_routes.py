from http import HTTPStatus

from fastapi import APIRouter


from api_mensagens.schemas.user import UserPublic, UserCreate, UserUpdate
from api_mensagens.core.security import Session, CurrentUser
from api_mensagens.services.user_service import (
    create_user_service,
    update_me_service,
    delete_me_service,
    delete_user_service,
    update_user_service,
)

router = APIRouter()


@router.post("", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate, session: Session):
    return create_user_service(user, session)


@router.get("/me", response_model=UserPublic)
def get_me(current_user: CurrentUser):
    return current_user


@router.patch("/me", response_model=UserPublic)
def update_me(
    user: UserUpdate,
    session: Session,
    current_user: CurrentUser,
):
    return update_me_service(user, session, current_user)


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(
    user: UserUpdate,
    session: Session,
    current_user: CurrentUser,
    user_id: int,
):
    return update_user_service(session, user, current_user, user_id)


@router.delete("/me")
def delete_me(
    session: Session,
    current_user: CurrentUser,
):
    return delete_me_service(session, current_user)


@router.delete("/{user_id}")
def delete_user(session: Session, current_user: CurrentUser, user_id: int):
    return delete_user_service(session, current_user, user_id)
