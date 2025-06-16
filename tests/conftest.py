import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from api_mensagens.db.base import table_registry
from api_mensagens.db.session import get_session
from sqlalchemy.orm import Session
from api_mensagens.main import app
from api_mensagens.models.user import User
from api_mensagens.models.message import Message
from api_mensagens.core.security import get_password_hash, get_current_user

@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    password = "testtest"
    user = User(
        username="test",
        email="test@test.com",
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def message(session):
    message = Message(content="Baesse")

    session.add(message)
    session.commit()
    session.refresh(message)

    return message


@pytest.fixture
def token(client, user):
    response = client.post(
        "auth/token",
        data={"username": user.email, "password": user.clean_password},
    )

    return response.json()["access_token"]

@pytest.fixture
def current_user(session, token):

    user = get_current_user(session, token)

    return user