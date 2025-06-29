from datetime import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api_mensagens.db.base import table_registry
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .user import User
    from .message import Message


@table_registry.mapped_as_dataclass
class Comment:
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, nullable=False, server_default=func.now()
    )
    
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    author: Mapped[Optional["User"]] = relationship("User", back_populates="comments", init=False)
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"), nullable=False)
    message: Mapped[Optional["Message"]] = relationship("Message", back_populates="comments", init=False)