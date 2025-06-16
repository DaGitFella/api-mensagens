from fastapi import APIRouter, Query
from typing import Annotated
from api_mensagens.services import message_service
from api_mensagens.schemas.message import PublicMessage, ListMessages, MessageCreate
from http import HTTPStatus
from api_mensagens.schemas.utils import FilterPage
from api_mensagens.core.security import session

router = APIRouter()

@router.post("", status_code=HTTPStatus.CREATED, response_model=PublicMessage)
def create_message(message: MessageCreate, db: session):
    return message_service.create_message(db, message)


@router.get("", response_model=ListMessages)
def get_messages(db: session, filter_page: Annotated[FilterPage, Query()]):
    messages = message_service.get_all_messages(db, filter_page)
    return {"messages": messages}


@router.get("/{message_id}", response_model=PublicMessage)
def get_one_message(message_id: int, db: session):
    return message_service.get_one_message(db, message_id)


@router.put("/{message_id}", response_model=PublicMessage)
def update_message(message_id: int, message: MessageCreate, db: session):
    return message_service.update_message(db, message_id, message)


@router.delete("/{message_id}")
def delete_message(message_id, db: session):
    return message_service.delete_message(db, message_id)
