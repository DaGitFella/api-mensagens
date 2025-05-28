from sqlalchemy import select

from api_mensagens.core.exceptions import get_or_404
from api_mensagens.models.message import Message
from api_mensagens.schemas.message import MessageCreate
from sqlalchemy.orm import Session

def create_message(db: Session, message: MessageCreate):
    db_message = Message(content=message.content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_all_messages(db: Session, limit: int, skip: int):
    return db.scalars(select(Message).offset(skip).limit(limit)).all()

def delete_message(db: Session, message_id: int):
    message = get_or_404(db, Message, message_id)
    db.delete(message)
    db.commit()
    return {'detail': f'message {message_id} was deleted'}

def get_one_message(db: Session, message_id: int):
    return get_or_404(db, Message, message_id)

def update_message(db: Session, message_id: int, message: MessageCreate):
    db_message = get_or_404(db, Message, message_id)

    db_message.content = message.content
    db.commit()
    db.refresh(db_message)
    return db_message
