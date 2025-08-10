from http import HTTPStatus


def test_create_message_must_return_201_and_message(client, token, headers):
    response = client.post(
        "/mensagens",
        headers=headers,
        json={
            "titulo": "A saga de amor de Baesse",
            "conteudo": "Baesse eu te amo",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "titulo": "A saga de amor de Baesse",
        "conteudo": "Baesse eu te amo",
        "id": 1,
        "usuario_id": 1,
    }


def test_create_message_must_return_401(client):
    response = client.post("/mensagens", json={"conteudo": "Testes vicenzo"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_create_message_with_invalid_content(client, token, headers):
    response = client.post("/mensagens", headers=headers, json={"conteudo": ""})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT


def test_get_messages_must_return_200_and_message(
    client,
    message,
):
    response = client.get("/mensagens")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "mensagens": [
            {
                "titulo": message.titulo,
                "conteudo": message.conteudo,
                "id": message.id,
                "usuario_id": message.usuario_id,
            }
        ]
    }


def tet_get_one_message_must_return_200_and_message(
    client, message, token, headers
):
    response = client.get(
        f"/mensagens/{message.id}",
        headers=headers,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == message


def test_get_message_must_return_401(client, message):
    response = client.get(
        "/mensagens/1",
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_message_must_return_200_and_message(
    client, message, token, headers
):
    response = client.put(
        f"/mensagens/{message.id}",
        headers=headers,
        json={
            "titulo": "A perda do amor de Baesse",
            "conteudo": "Baesse eu te odeio",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "titulo": "A perda do amor de Baesse",
        "conteudo": "Baesse eu te odeio",
        "id": message.id,
        "usuario_id": message.usuario_id,
    }


def test_update_message_with_partial_content_must_return_200_and_message(
    client, message, token, headers
):
    response = client.patch(
        f"/mensagens/{message.id}",
        headers=headers,
        json={
            "titulo": "A morte do rei gado",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": message.id,
        "titulo": "A morte do rei gado",
        "conteudo": message.conteudo,
        "usuario_id": message.usuario_id,
        "comentarios": [],
    }


def test_delete_message_must_return_200_and_detail(
    client, message, token, headers
):
    response = client.delete(f"/mensagens/{message.id}", headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "detail": f"message {message.id} was deleted",
    }


def test_delete_other_message_must_return_403_and_detail(
    client, message, message_2, token, headers
):
    response = client.delete(f"/mensagens/{message_2.id}", headers=headers)

    assert response.status_code == HTTPStatus.FORBIDDEN
