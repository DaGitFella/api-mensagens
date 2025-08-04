import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from api_mensagens.db.base import table_registry
from api_mensagens.db.session import get_session
from sqlalchemy.orm import Session
from api_mensagens.main import app
from api_mensagens.models.user import User
from api_mensagens.models.message import Message
from api_mensagens.models.comment import Comment
from api_mensagens.core.security import get_password_hash


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
        nome="test",
        email="test@test.com",
        senha=get_password_hash(password),
        mensagens=[],
        comentarios=[],
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def user_2(session):
    password = "lucas"
    user_2 = User(
        nome="lucas",
        email="lucas@gmail.com",
        senha=get_password_hash(password),
        mensagens=[],
        comentarios=[],
    )
    session.add(user_2)
    session.commit()
    session.refresh(user_2)

    user_2.clean_password = password

    return user_2


@pytest.fixture
def message(session, user):
    message = Message(
        titulo="A odisséia de Baesse",
        conteudo="Baesse",
        id_usuario=user.id,
        usuario=user,
        comentarios=[]
    )
    session.add(message)
    session.commit()
    session.refresh(message)

    return message


@pytest.fixture
def message_2(session, user_2):
    message = Message(
        titulo="A odisséia de Baesse",
        conteudo="Baesse",
        id_usuario=user_2.id,
        usuario=user_2,
        comentarios=[],
    )
    session.add(message)
    session.commit()
    session.refresh(message)

    return message


@pytest.fixture
def comment(session, message, user):
    comment = Comment(
        conteudo="eu odeio essa messagem. Apague",
        id_usuario=user.id,
        id_mensagem=message.id,
    )

    session.add(comment)
    session.commit()
    session.refresh(comment)

    return comment


@pytest.fixture
def token(client, user):
    response = client.post(
        "auth/login",
        data={"username": user.email, "password": user.clean_password},
    )

    return response.json()


@pytest.fixture
def headers(token):
    return {"Authorization": f"Bearer {token['access_token']}"}
