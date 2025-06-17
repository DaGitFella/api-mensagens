from http import HTTPStatus
from fastapi import APIRouter


from api_mensagens.schemas.user import UserPublic, UserCreate, UserUpdate
from api_mensagens.core.security import Session, CurrentUser
from api_mensagens.services.user_service import (

    create_user_service, 
    get_me_service, 
    update_me_service,
    delete_me_service
)

router = APIRouter()


@router.post("", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate, session: Session):
    return create_user_service(user, session)


@router.get("/me", response_model=UserPublic)
def get_me(session: Session, current_user: CurrentUser):
    return get_me_service(session, current_user)


@router.put("/me", response_model=UserPublic)
def update_me( user: UserUpdate, session: Session,current_user: CurrentUser,):
    return update_me_service(user, session, current_user)

@router.delete("/me")
def delete_me( session: Session, current_user: CurrentUser,):
    return delete_me_service(session, current_user)
