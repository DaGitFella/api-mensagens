from fastapi import APIRouter, Path
from http import HTTPStatus

from api_mensagens.schemas.comment import (
    CommentCreate,
    PublicComment,
    ListComments,
    CommentUpdate,
)
from api_mensagens.core.security import Session, CurrentUser
from api_mensagens.services.comment_service import (
    create_comment_service,
    list_comments_by_message_service,
    delete_comment_service,
    update_comment_service,
)

router = APIRouter()


@router.post(
    "/{message_id}",
    status_code=HTTPStatus.CREATED,
    response_model=PublicComment,
)
def create_comment(
    message_id: int = Path(..., description="ID of the message to comment on"),
    comment: CommentCreate = ...,
    db: Session = ...,              # será injetado pelo FastAPI
    current_user: CurrentUser = ...,
):
    return create_comment_service(db, message_id, comment, current_user)


@router.get(
    "/{message_id}",
    response_model=ListComments,
)
def list_comments_by_message(
    message_id: int = Path(..., description="ID of the message"),
    db: Session = ...,
):
    comments = list_comments_by_message_service(db, message_id)
    return {"comments": comments}


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int = Path(..., description="ID of the comment"),
    db: Session = ...,
    current_user: CurrentUser = ...,
):
    return delete_comment_service(db, comment_id, current_user)


@router.put("/{comment_id}", response_model=PublicComment)
def update_comment(
    comment_id: int = Path(..., description="ID of the comment to update"),
    updated: CommentUpdate = ...,
    db: Session = ...,
    current_user: CurrentUser = ...,
):
    return update_comment_service(db, comment_id, updated, current_user)
