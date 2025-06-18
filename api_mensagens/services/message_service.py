from typing import Annotated

from fastapi import Query, HTTPException, Depends
from sqlalchemy import select

from api_mensagens.core.exceptions import get_or_404
from api_mensagens.models.message import Message
from api_mensagens.schemas.message import MessageCreate
from api_mensagens.schemas.utils import FilterPage
from api_mensagens.core.security import Session, CurrentUser, get_current_user


def create_message(db: Session, message: MessageCreate, current_user: CurrentUser = Depends(get_current_user)):
    db_message = Message(content=message.content, user_id = current_user.id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


#def get_all_messages(db: Session, filter_page: Annotated[FilterPage, Query()]):
def get_all_messages(db: Session, filter_page: FilterPage, current_user: CurrentUser = Depends(get_current_user)):
    return db.scalars(
        select(Message).where(Message.user_id == current_user.id).offset(filter_page.offset).limit(filter_page.limit)
    ).all()


def get_one_message(db: Session, message_id: int, current_user: CurrentUser = Depends(get_current_user)):
    message = get_or_404(db, Message, message_id)
    if message.user_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "You don't have permission to access this message")
    return message


def delete_message(db: Session, message_id: int, current_user: CurrentUser = Depends(get_current_user)):
    message = get_or_404(db, Message, message_id)
    if message.user_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "You can't delete this message")
    db.delete(message)
    db.commit()
    return {"detail": f"message {message_id} was deleted"}


def update_message(db: Session, message_id: int, message: MessageCreate, current_user: CurrentUser = Depends(get_current_user)):
    db_message = get_or_404(db, Message, message_id)
    if db_message.user_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "You can't edit this message")
    db_message.content = message.content
    db.commit()
    db.refresh(db_message)
    return db_message
