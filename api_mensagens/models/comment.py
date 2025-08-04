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
    __tablename__ = "comentarios"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    conteudo: Mapped[str] = mapped_column(nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(
        init=False, nullable=False, server_default=func.now()
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), nullable=False
    )
    autor: Mapped[Optional["User"]] = relationship(
        "User", back_populates="comentarios", init=False
    )
    mensagem_id: Mapped[int] = mapped_column(
        ForeignKey("mensagens.id"), nullable=False
    )
    mensagem: Mapped[Optional["Message"]] = relationship(
        "Message", back_populates="comentarios", init=False
    )
