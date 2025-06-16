from http import HTTPStatus


def test_create_message_must_return_201_and_message(client):
    response = client.post("/messages", json={"content": "Baesse eu te amo"})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"content": "Baesse eu te amo", "id": 1}


def test_create_message_with_invalid_content(client):
    response = client.post("/messages", json={"content": ""})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT


def test_get_one_message_must_return_200_and_message(client, message):
    response = client.get(f"/messages/{message.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "content": message.content,
        "id": message.id,
    }


def test_get_messages_must_return_200_and_message(client, message):
    response = client.get("/messages")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "messages": [
            {
                "content": message.content,
                "id": message.id,
            }
        ]
    }


def test_get_message_must_return_404(client):
    response = client.get("/messages/2")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_message_must_return_200_and_message(client, message):
    response = client.put(
        f"/messages/{message.id}", json={"content": "Baesse eu te odeio"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "content": "Baesse eu te odeio",
        "id": message.id,
    }


def test_delete_message_must_return_200_and_detail(client, message):
    response = client.delete(f"/messages/{message.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "detail": f"message {message.id} was deleted",
    }
