from sqlalchemy import select

from api_mensagens.core.exceptions import (
    get_or_404,
    credentials_exception,
    not_found_exception, forbidden_exception,
)
from api_mensagens.models.comment import Comment
from api_mensagens.models.message import Message
from api_mensagens.schemas.comment import CommentCreate, CommentUpdate
from api_mensagens.core.security import Session, CurrentUser


def create_comment_service(
    db: Session,
    id_mensagem: int,
    comment_data: CommentCreate,
    current_user: CurrentUser,
):
    message = db.scalar(select(Message).where(Message.id == id_mensagem))
    if not message:
        raise not_found_exception(detail="Message not found.")

    comment = Comment(
        conteudo=comment_data.conteudo,
        usuario_id=current_user.id,
        mensagem_id=id_mensagem,
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def list_comments_by_message_service(db: Session, id_mensagem: int):
    message = db.scalar(select(Message).where(Message.id == id_mensagem))
    if not message:
        raise not_found_exception(detail="Message not found.")

    return db.scalars(
        select(Comment).where(Comment.mensagem_id == id_mensagem)
    ).all()


def update_comment_service(
    db: Session,
    comment_id: int,
    comment_data: CommentUpdate,
    current_user: CurrentUser,
):
    comment: Comment = get_or_404(db, Comment, comment_id, "comment")

    if (
        current_user.perfil != "ADMIN"
        and comment.usuario_id != current_user.id
    ):
        raise forbidden_exception(
            detail="You can only update your own comments."
        )

    comment.conteudo = comment_data.conteudo
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment_service(
    db: Session,
    comment_id: int,
    current_user: CurrentUser,
):
    comment: Comment = get_or_404(db, Comment, comment_id, "comment")

    if (
        current_user.perfil != "ADMIN"
        and comment.usuario_id != current_user.id
    ):
        raise forbidden_exception(
            detail="You can only delete your own comments."
        )

    if not comment:
        raise not_found_exception(detail="Comment not found.")

    db.delete(comment)
    db.commit()
    return {"detail": f"Comment {comment_id} deleted."}
