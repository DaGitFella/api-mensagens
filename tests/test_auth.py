from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        "auth/login",
        data={"username": user.email, "password": user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "refresh_token" in token


def test_get_token_with_wrong_email(client, user):
    response = client.post(
        "auth/login",
        data={"username": "fodaci", "password": user.clean_password},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_token_with_wrong_password(client, user):
    response = client.post(
        "auth/login",
        data={"username": user.email, "password": "<PASSWORD>"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_new_token(client, token):
    response = client.post(
        "auth/refresh", json={"refresh_token": token["refresh_token"]}
    )

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()
