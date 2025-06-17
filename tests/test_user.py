from http import HTTPStatus


def test_get_all_users(client):
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK


def test_create_user_must_return_201(client):
    response = client.post(
        "/users",
        json={
            "email": "lucas@gmail.com",
            "username": "lucas",
            "password": "Pa7!45sada",
        },
    )

    assert response.status_code == HTTPStatus.CREATED


def test_create_user_must_return_409(client, user):
    response = client.post(
        "/users",
        json={
            "email": user.email,
            "username": user.username,
            "password": "Pa7!45sada",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_get_current_user_must_return_200(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)

    assert response.status_code == HTTPStatus.OK


def test_update_current_user_must_return_200(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        "/users/me",
        headers=headers,
        json={
            "username": "lucas",
            "email": "lula@gmail.com",
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_update_user_must_return_409(client, token, user_2):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        "/users/me",
        headers=headers,
        json={"username": "lucas", "email": user_2.email},
    )

    assert response.status_code == HTTPStatus.CONFLICT
