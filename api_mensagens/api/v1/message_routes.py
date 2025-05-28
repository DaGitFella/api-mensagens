from fastapi import APIRouter, Depends
from api_mensagens.services import message_service
from api_mensagens.db.session import get_session
from sqlalchemy.orm import Session
from api_mensagens.schemas.message import PublicMessage, ListMessages, MessageCreate
from typing import List
from http import HTTPStatus

router = APIRouter()


@router.post('', status_code=HTTPStatus.CREATED, response_model=PublicMessage)
def create_message(message: MessageCreate, db: Session = Depends(get_session)):
    return message_service.create_message(db, message)

@router.get('', response_model=ListMessages)
def get_messages(db: Session = Depends(get_session)):
    messages =message_service.get_all_messages(db)
    return {'messages': messages}

@router.get('/{message_id}', response_model=PublicMessage)
def get_one_message(message_id: int, db: Session = Depends(get_session)):
    return message_service.get_one_message(db, message_id)

@router.put('/{message_id}', response_model=PublicMessage)
def update_message(message_id: int, message: MessageCreate, db: Session = Depends(get_session)):
    return message_service.update_message(db, message_id, message)

@router.delete("/{message_id}")
def delete_message(message_id, db: Session = Depends(get_session)):
    return message_service.delete_message(db, message_id)