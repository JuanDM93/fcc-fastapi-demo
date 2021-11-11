import pytest
from jose import jwt

from app import schemas
from app.config import settings


# def test_root(client):
#     response = client.get("/")
#     assert response.json() == {"message": "Hello World!"}
#     assert response.status_code == 200


def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "test_user@mail.com", "password": "test_password"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "test_user@mail.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user['email'], "password": test_user['password']})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(
        login_response.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrong@mail.com", "test_password", 401),
        ("test_user@mail.com", "wrong_password", 401),
        (None, "test_password", 422),
        ("test_user@mail.com", None, 422),
    ]
)
def test_incorrect_login(client, email, password, status_code):
    response = client.post(
        "/login", data={"username": email, "password": password})
    assert response.status_code == status_code
