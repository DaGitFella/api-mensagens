from datetime import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api_mensagens.db.base import table_registry
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .user import User
    from .comment import Comment


@table_registry.mapped_as_dataclass
class Message:
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, nullable=False, server_default=func.now()
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="messages")
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="message", cascade="all, delete-orphan"
    )
