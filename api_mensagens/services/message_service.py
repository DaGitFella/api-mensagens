from sqlalchemy import select

from api_mensagens.core.exceptions import (
    get_or_404,
    credentials_exception,
    not_found_exception,
    forbidden_exception,
)
from api_mensagens.models.message import Message
from api_mensagens.schemas.message import MessageCreate, MessagePatch
from api_mensagens.schemas.utils import FilterPage
from api_mensagens.core.security import Session, CurrentUser


def create_message(
    db: Session, message: MessageCreate, current_user: CurrentUser
):
    db_message = Message(
        title=message.title,
        content=message.content,
        user_id=current_user.id,
        user=current_user,
        comments=[],
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_all_messages(db: Session, filter_page: FilterPage):
    return db.scalars(
        select(Message).offset(filter_page.offset).limit(filter_page.limit)
    ).all()


def get_message(db: Session, message_id: int, current_user: CurrentUser):
    message = get_or_404(db=db, resource=Message, object_id=message_id)
    return message


def get_my_messages(db: Session, current_user: CurrentUser):
    messages = db.scalars(
        select(Message).where(Message.user_id == current_user.id)
    ).all()

    if not messages:
        raise not_found_exception(
            detail="Messages not found.",
        )

    return {"messages": messages}


def delete_message(db: Session, message_id: int, current_user: CurrentUser):
    message = get_or_404(
        db, Message, object_id=message_id, resource_name="message"
    )

    if not current_user.is_staff and message.user_id != current_user.id:
        raise forbidden_exception(
            detail="You don't have permission to access this message"
        )

    db.delete(message)
    db.commit()
    return {"detail": f"message {message_id} was deleted"}


def update_message(
    db: Session,
    message_id: int,
    message: MessageCreate,
    current_user: CurrentUser,
):
    db_message = get_or_404(
        db, Message, object_id=message_id, resource_name="message"
    )

    if not current_user.is_staff and db_message.user_id != current_user.id:
        raise credentials_exception(
            detail="You don't have permission to access this message"
        )

    db_message.title = message.title
    db_message.content = message.content
    db.commit()
    db.refresh(db_message)
    return db_message


def change_message(
    db: Session,
    message_id: int,
    message: MessagePatch,
    current_user: CurrentUser,
):
    db_message = get_or_404(
        db, Message, object_id=message_id, resource_name="message"
    )

    if not current_user.is_staff and db_message.user_id != current_user.id:
        raise credentials_exception(
            detail="You don't have permission to access this message"
        )

    if message.title:
        db_message.title = message.title

    if message.content:
        db_message.content = message.content

    db.commit()
    db.refresh(db_message)
    return db_message
