from http import HTTPStatus


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


def test_create_user_with_invalid_password(client):
    response = client.post(
        "/users",
        json={
            "email": "pedro@pedro.com",
            "username": "ruan",
            "password": "pedro",
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


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


def test_get_current_user_must_return_200(client, token, headers):
    response = client.get("/users/me", headers=headers)

    assert response.status_code == HTTPStatus.OK


def test_update_current_user_must_return_200(client, token, headers):
    response = client.patch(
        "/users/me",
        headers=headers,
        json={
            "username": "lucas",
            "email": "lula@gmail.com",
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_update_user_with_partial_data_must_return_200(client, token, headers):
    response = client.patch(
        "/users/me",
        headers=headers,
        json={
            "username": "lucas",
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_update_user_must_return_409(client, token, user_2, headers):
    response = client.patch(
        "/users/me",
        headers=headers,
        json={"username": "lucas", "email": user_2.email},
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_delete_user_must_return_200(client, token, headers):
    response = client.delete("/users/me", headers=headers)

    assert response.status_code == HTTPStatus.OK
