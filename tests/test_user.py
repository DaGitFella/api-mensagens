from http import HTTPStatus


def test_create_user_must_return_201(client):
    response = client.post(
        "/usuarios",
        json={
            "email": "lucas@gmail.com",
            "nome": "lucas",
            "senha": "Pa7!45sada",
        },
    )

    assert response.status_code == HTTPStatus.CREATED


def test_create_user_with_invalid_senha(client):
    response = client.post(
        "/usuarios",
        json={
            "email": "pedro@pedro.com",
            "nome": "ruan",
            "senha": "pedro",
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user_must_return_409(client, user):
    response = client.post(
        "/usuarios",
        json={
            "email": user.email,
            "nome": user.nome,
            "senha": "Pa7!45sada",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_get_current_user_must_return_200(client, token, headers):
    response = client.get("/usuarios/me", headers=headers)

    assert response.status_code == HTTPStatus.OK


def test_update_current_user_must_return_200(client, token, headers):
    response = client.patch(
        "/usuarios/me",
        headers=headers,
        json={
            "nome": "lucas",
            "email": "lula@gmail.com",
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_update_user_with_partial_data_must_return_200(client, token, headers):
    response = client.patch(
        "/usuarios/me",
        headers=headers,
        json={
            "nome": "lucas",
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_update_user_must_return_409(client, token, user_2, headers):
    response = client.patch(
        "/usuarios/me",
        headers=headers,
        json={"nome": "lucas", "email": user_2.email},
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_delete_user_must_return_200(client, token, headers):
    response = client.delete("/usuarios/me", headers=headers)

    assert response.status_code == HTTPStatus.OK
