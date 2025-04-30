from api_mensagens.db.session import engine
from api_mensagens.db.base import Base

def init_db():
    Base.metadata.create_all(bind=engine)