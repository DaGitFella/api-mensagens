from sqlalchemy import select

from api_mensagens.models.message import Message
from api_mensagens.schemas.message import MessageCreate
from sqlalchemy.orm import Session

from api_mensagens.services import error_handler_service

def create_message(db: Session, message: MessageCreate):
    content = error_handler_service.get_content_or_bad_request(message)
    db_message = Message(content=content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_all_messages(db: Session):
    return db.scalars(select(Message)).all()

def delete_message(db: Session, message_id: int):
    message = error_handler_service.get_object_or_not_found(db, Message, message_id)
    db.delete(message)
    db.commit()
    return {'detail': f'message {message_id} was deleted'}

def get_one_message(db: Session, message_id: int):
    message = error_handler_service.get_object_or_not_found(db, Message, message_id)
    return message

def update_message(db: Session, message_id: int, message: MessageCreate):
    db_message = error_handler_service.get_object_or_not_found(db, Message, message_id)
    content = error_handler_service.get_content_or_bad_request(message)
    db_message.content = content
    db.commit()
    db.refresh(db_message)
    return db_message
