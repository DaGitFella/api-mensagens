from api_mensagens.models.message import Message
from api_mensagens.schemas.message import MessageCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException

def create_message(db: Session, message: MessageCreate):
    db_message = Message(content=message.content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_all_messages(db: Session):
    return db.query(Message).all()

def delete_message(db: Session, message_id: int):
    deleted_message = db.query(Message).filter(Message.id == message_id).first()
    if not deleted_message:
        raise HTTPException(404, detail='o id não existe')

    db.delete(deleted_message)
    db.commit()
    return deleted_message

def get_one_message(db: Session, message_id: int):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(404, detail='o id não existe')

    return message

def update_message(db: Session, message_id: int, message: MessageCreate):
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if not db_message:
        raise HTTPException(404, detail='o id não existe')

    db_message.content = message.content
    db.commit()
    db.refresh(db_message)
    return db_message
