from http import HTTPStatus

from jwt import decode

from api_mensagens.core.security import create_access_token, settings


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['test'] == 'test'
    assert 'exp' in decoded

def test_get_current_user(client, current_user):
    response = client.get("/users/me")
    assert response.status_code == HTTPStatus.OK
    assert current_user.id == response.json().get('id')