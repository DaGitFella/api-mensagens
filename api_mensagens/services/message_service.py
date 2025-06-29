from sqlalchemy import select

from api_mensagens.core.exceptions import get_or_404, credentials_exception
from api_mensagens.models.message import Message
from api_mensagens.schemas.message import MessageCreate
from api_mensagens.schemas.utils import FilterPage
from api_mensagens.core.security import Session, CurrentUser


def create_message(db: Session, message: MessageCreate, current_user: CurrentUser):
    db_message = Message(content=message.content, user_id=current_user.id, user=current_user)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


# def get_all_messages(db: Session, filter_page: Annotated[FilterPage, Query()]):
def get_all_messages(db: Session, filter_page: FilterPage, current_user: CurrentUser):
    return db.scalars(
        select(Message)
        .offset(filter_page.offset)
        .limit(filter_page.limit)
    ).all()


def get_one_message(db: Session, message_id: int, current_user: CurrentUser):
    message = get_or_404(db, Message, object_id=message_id, resource_name='message')
    if message.user_id != current_user.id:
        raise credentials_exception(
            detail="You don't have permission to access this message"
        )
    return message


def delete_message(db: Session, message_id: int, current_user: CurrentUser):
    message = get_or_404(db, Message, object_id=message_id, resource_name='message')
    if message.user_id != current_user.id:
        raise credentials_exception(
            detail="You don't have permission to access this message"
        )
    db.delete(message)
    db.commit()
    return {"detail": f"message {message_id} was deleted"}


def update_message(
    db: Session, message_id: int, message: MessageCreate, current_user: CurrentUser
):
    db_message = get_or_404(db, Message, object_id=message_id, resource_name='message')
    if db_message.user_id != current_user.id:
        raise credentials_exception(
            detail="You don't have permission to access this message"
        )
    db_message.content = message.content
    db.commit()
    db.refresh(db_message)
    return db_message
