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
    __tablename__ = "mensagens"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    titulo: Mapped[str] = mapped_column(nullable=False)
    conteudo: Mapped[str] = mapped_column(nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(
        init=False, nullable=False, server_default=func.now()
    )
    curtidas: Mapped[int] = mapped_column(
        init=False, nullable=False,
        server_default='0'
    )
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), nullable=False
    )
    usuario: Mapped["User"] = relationship("User", back_populates="mensagens")
    comentarios: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="mensagem", cascade="all, delete-orphan"
    )
