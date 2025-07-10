from fastapi import APIRouter, Query
from typing import Annotated
from api_mensagens.services import message_service
from api_mensagens.schemas.message import (
    PublicMessage,
    ListMessages,
    MessageCreate,
)
from http import HTTPStatus
from api_mensagens.schemas.utils import FilterPage
from api_mensagens.core.security import Session, CurrentUser, adminRequired

router = APIRouter()


@router.post("", status_code=HTTPStatus.CREATED, response_model=PublicMessage)
def create_message(
    message: MessageCreate, db: Session, current_user: CurrentUser
):
    return message_service.create_message(db, message, current_user)


@router.get("", response_model=ListMessages)
def get_messages(
    db: Session,
    filter_page: Annotated[FilterPage, Query()],
):
    messages = message_service.get_all_messages(db, filter_page)
    return {"messages": messages}


@router.get("/me", response_model=ListMessages)
def get_my_message(db: Session, current_user: CurrentUser):
    return message_service.get_my_messages(db, current_user)


@router.put("/{message_id}", response_model=PublicMessage)
def update_message(
    message_id: int,
    message: MessageCreate,
    db: Session,
    current_user: CurrentUser,
):
    return message_service.update_message(
        db, message_id, message, current_user
    )


@router.delete("/{message_id}")
def delete_message(message_id, db: Session, current_user: CurrentUser):
    return message_service.delete_message(db, message_id, current_user)
