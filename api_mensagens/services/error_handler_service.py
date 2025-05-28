from http.client import HTTPException

from http import HTTPStatus
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from api_mensagens.schemas.message import MessageCreate


def get_object_or_not_found(
    session: Session, 
    model,
    id_: int,
):
    stmt = select(model).where(model.id == id_)
    obj = session.scalar(stmt)
    if not obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Item not found')
    return obj

def get_content_or_bad_request(
    model: MessageCreate,
):
    content = model.content
    if not content:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='You must provide a content')
    return content