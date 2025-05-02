from fastapi import APIRouter, Depends
from api_mensagens.services import message_service
from api_mensagens.api.deps import get_db
from sqlalchemy.orm import Session
from api_mensagens.schemas.message import MessageCreate
from typing import List
from http import HTTPStatus

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=MessageCreate)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    return message_service.create_message(db, message)

@router.get('/', response_model=List[MessageCreate])
def get_messages(db: Session = Depends(get_db)):
    return message_service.get_all_messages(db)

@router.get('/{message_id}')
def get_one_message(message_id: int, db: Session = Depends(get_db)):
    return message_service.get_one_message(db, message_id)

@router.put('/{message_id}')
def update_message(message_id: int, message: MessageCreate, db: Session = Depends(get_db)):
    return message_service.update_message(db, message_id, message)

@router.delete("/{message_id}")
def delete_message(message_id, db: Session = Depends(get_db)):
    return message_service.delete_message(db, message_id)