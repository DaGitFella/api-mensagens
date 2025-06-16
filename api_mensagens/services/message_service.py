from typing import Annotated

from fastapi import Query
from sqlalchemy import select

from api_mensagens.core.exceptions import get_or_404
from api_mensagens.models.message import Message
from api_mensagens.schemas.message import MessageCreate
from api_mensagens.schemas.utils import FilterPage
from api_mensagens.core.security import session


def create_message(db: session, message: MessageCreate):
    db_message = Message(content=message.content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_all_messages(db: session, filter_page: Annotated[FilterPage, Query()]):
    return db.scalars(
        select(Message).offset(filter_page.offset).limit(filter_page.limit)
    ).all()


def delete_message(db: session, message_id: int):
    message = get_or_404(db, Message, message_id)
    db.delete(message)
    db.commit()
    return {"detail": f"message {message_id} was deleted"}


def get_one_message(db: session, message_id: int):
    return get_or_404(db, Message, message_id)


def update_message(db: session, message_id: int, message: MessageCreate):
    db_message = get_or_404(db, Message, message_id)

    db_message.content = message.content
    db.commit()
    db.refresh(db_message)
    return db_message
