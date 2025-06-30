from sqlalchemy import select

from api_mensagens.core.exceptions import (
    get_or_404,
    credentials_exception,
    not_found_exception,
)
from api_mensagens.models.comment import Comment
from api_mensagens.models.message import Message
from api_mensagens.schemas.comment import CommentCreate, CommentUpdate
from api_mensagens.core.security import Session, CurrentUser


def create_comment_service(
    db: Session,
    message_id: int,
    comment_data: CommentCreate,
    current_user: CurrentUser,
):
    message = db.scalar(select(Message).where(Message.id == message_id))
    if not message:
        raise not_found_exception(detail="Message not found.")

    comment = Comment(
        content=comment_data.content,
        author_id=current_user.id,
        message_id=message_id,
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def list_comments_by_message_service(db: Session, message_id: int):
    message = db.scalar(select(Message).where(Message.id == message_id))
    if not message:
        raise not_found_exception(detail="Message not found.")

    return db.scalars(
        select(Comment).where(Comment.message_id == message_id)
    ).all()


def update_comment_service(
    db: Session,
    comment_id: int,
    comment_data: CommentUpdate,
    current_user: CurrentUser,
):
    comment = get_or_404(db, Comment, comment_id, "comment")

    if comment.author_id != current_user.id:
        raise credentials_exception(
            detail="You can only update your own comments."
        )

    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment_service(
    db: Session,
    comment_id: int,
    current_user: CurrentUser,
):
    comment = get_or_404(db, Comment, comment_id, "comment")

    if comment.author_id != current_user.id:
        raise credentials_exception(
            detail="You can only delete your own comments."
        )

    if not comment:
        raise not_found_exception(
            detail="Comment not found."
        )

    db.delete(comment)
    db.commit()
    return {"detail": f"Comment {comment_id} deleted."}
