from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api_mensagens.core.config import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, bind=engine)


def get_session():
    with SessionLocal() as session:  # pragma: no cover
        yield session
