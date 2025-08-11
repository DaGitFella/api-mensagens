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
        titulo=message.titulo,
        conteudo=message.conteudo,
        usuario_id=current_user.id,
        usuario=current_user,
        comentarios=[],
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
        select(Message).where(Message.usuario_id == current_user.id)
    ).all()

    if not messages:
        raise not_found_exception(
            detail="Messages not found.",
        )

    return {"messages": messages}


def delete_message(db: Session, message_id: int, current_user: CurrentUser):
    message: Message = get_or_404(
        db, Message, object_id=message_id, resource_name="message"
    )

    if (
        current_user.perfil != "ADMIN"
        and message.usuario_id != current_user.id
    ):
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
    db_message: Message = get_or_404(
        db, Message, object_id=message_id, resource_name="message"
    )

    if (
        current_user.perfil != "ADMIN"
        and db_message.usuario_id != current_user.id
    ):
        raise credentials_exception(
            detail="You don't have permission to access this message"
        )

    db_message.titulo = message.titulo
    db_message.conteudo = message.conteudo
    db.commit()
    db.refresh(db_message)
    return db_message


def change_message(
    db: Session,
    message_id: int,
    message: MessagePatch,
    current_user: CurrentUser,
):
    db_message: Message = get_or_404(
        db, Message, object_id=message_id, resource_name="message"
    )

    if (
        current_user.perfil != "ADMIN"
        and db_message.usuario_id != current_user.id
    ):
        raise credentials_exception(
            detail="You don't have permission to access this message"
        )

    if message.titulo:
        db_message.titulo = message.titulo

    if message.conteudo:
        db_message.conteudo = message.conteudo

    db.commit()
    db.refresh(db_message)
    return db_message
