from http import HTTPStatus


def test_create_message_must_return_201_and_message(client, token, headers):
    response = client.post(
        "/messages", headers=headers, json={"title": "A saga de amor de Baesse",
                                            "content": "Baesse eu te amo"}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"title": "A saga de amor de Baesse",
                               "content": "Baesse eu te amo", "id": 1}


def test_create_message_must_return_401(client):
    response = client.post(
        '/messages',
        json = {"content": "Testes vicenzo"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_create_message_with_invalid_content(client, token, headers):
    response = client.post("/messages", headers=headers, json={"content": ""})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT


def test_get_messages_must_return_200_and_message(
    client, message,
):
    response = client.get("/messages")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "messages": [
            {
                "title": message.title,
                "content": message.content,
                "id": message.id,
            }
        ]
    }


def tet_get_one_message_must_return_200_and_message(client, message, token, headers):
    response = client.get(
        f'/messages/{message.id}',
        headers=headers,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == message


def test_get_message_must_return_401(client, message):
    response = client.get(
        '/messages/1',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_update_message_must_return_200_and_message(
    client, message, token, headers
):
    response = client.put(
        f"/messages/{message.id}",
        headers=headers,
        json={'title':'A perda do amor de Baesse',
              "content": "Baesse eu te odeio"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'title': 'A perda do amor de Baesse',
        "content": "Baesse eu te odeio",
        "id": message.id,
    }


def test_delete_message_must_return_200_and_detail(
    client, message, token, headers
):
    response = client.delete(f"/messages/{message.id}", headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "detail": f"message {message.id} was deleted",
    }
