from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api_mensagens.core.config import Settings

engine = create_engine(Settings().DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, bind=engine)

def get_session():
    with SessionLocal() as session:
        yield session
