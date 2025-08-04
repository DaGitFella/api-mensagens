from http import HTTPStatus


def test_create_comment_must_return_201(client, token, message, headers):
    response = client.post(
        f"/messages/{message.id}/comments",
        headers=headers,
        json={"content": "eu gosto dessa mensagem"},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "content": "eu gosto dessa mensagem",
        "author_id": 1,
        "message_id": message.id,
    }


def test_get_message_comments_must_return_200_and_comments(
    client, message, comment
):
    response = client.get(
        f"/messages/{message.id}/comments",
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "comments": [
            {
                "id": comment.id,
                "content": comment.content,
                "author_id": comment.author_id,
                "message_id": comment.message_id,
            }
        ]
    }


def test_delete_comment_must_return_200(
    client, token, headers, message, comment
):
    response = client.delete(
        f"/messages/{message.id}/comments/{comment.id}", headers=headers
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"detail": f"Comment {comment.id} deleted."}


def test_update_comment_must_return_200(
    client, token, headers, comment, message
):
    response = client.put(
        f"/messages/{message.id}/comments/{comment.id}",
        headers=headers,
        json={"content": "eu gosto dessa mensagem"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": comment.id,
        "content": "eu gosto dessa mensagem",
        "author_id": comment.author_id,
        "message_id": comment.message_id,
    }
