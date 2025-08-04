from datetime import datetime
from typing import List

from sqlalchemy import func

from api_mensagens.db.base import table_registry
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .message import Message
from .comment import Comment


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    mensagens: Mapped[List["Message"]] = relationship(
        "Message", back_populates="usuario", cascade="all, delete-orphan"
    )
    comentarios: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="autor"
    )
    perfil: Mapped[str] = mapped_column(
        nullable=False,
        server_default="USUARIO",
        default="USUARIO",
    )
