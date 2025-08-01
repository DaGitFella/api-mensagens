from datetime import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy.sql import expression

from api_mensagens.db.base import table_registry
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .message import Message
from .comment import Comment


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_staff: Mapped[bool] = mapped_column(
        nullable=False,
        init=False,
        server_default=expression.false(),
        default=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="user", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="author"
    )
