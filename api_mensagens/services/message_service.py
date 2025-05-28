from fastapi import HTTPException
from sqlalchemy import select

from api_mensagens.models.message import Message
from api_mensagens.schemas.message import MessageCreate
from sqlalchemy.orm import Session
from api_mensagens.core.exceptions import NotFoundException

def create_message(db: Session, message: MessageCreate):
    db_message = Message(content=message.content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_all_messages(db: Session):
    return db.scalars(select(Message)).all()

def delete_message(db: Session, message_id: int):
    message = db.get(Message, message_id)
    db.delete(message)
    db.commit()
    return {'detail': f'message {message_id} was deleted'}

def get_one_message(db: Session, message_id: int):
    message = db.get(Message, message_id)

    if not message:
        raise HTTPException(status_code=404, detail='Message not found')

    return message

def update_message(db: Session, message_id: int, message: MessageCreate):
    db_message = db.get(Message, message_id)

    db_message.content = message.content
    db.commit()
    db.refresh(db_message)
    return db_message
