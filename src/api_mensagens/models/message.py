from sqlalchemy import Column, Integer, String
from api_mensagens.db.base import Base

class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    content = Column(String(160), nullable=False)