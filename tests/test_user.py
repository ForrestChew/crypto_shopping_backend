from jose import jwt
from app import schemas
from app.config import settings
import pytest


@pytest.mark.parametrize(
    "email, password",
    [
        ("123@gmail.com", "password123"),
        ("skylarwhite@yahoo.com", "family"),
        ("saulgoodman@aol.net", "justice"),
    ],
)
def test_create_user(client, email, password):
    res = client.post("/users/", json={"email": email, "password": password})
    new_user = schemas.CreatedUser(**res.json())
    assert res.status_code == 201
    assert new_user.email == email


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token,
        settings.jose_jwt_secret_key,
        algorithms=[settings.algorithm],
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("123@gmail.com", "password123", "404"),
        ("skylarwhite@yahoo.com", "family", "404"),
        ("testuser@gmail.com", "potato", "403"),
        ("testuser@gmail.com", "838*$72$&@($", "403"),
    ],
)
def test_login_invalid_credentials(client, test_user, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    assert str(res.status_code) == status_code


def test_get_current_authed_user(authed_client):
    res = authed_client.get("/users/")
    user = schemas.CreatedUser(**res.json())
    assert res.status_code == 200
    assert user.email == "testuser@gmail.com"


def test_get_user_unauthorized(client):
    res = client.get("/users/")
    assert res.status_code == 401


def test_delete_user(authed_client, test_user):
    res = authed_client.delete("/users/")
    assert res.status_code == 204


def test_delete_user_unauthorized(client, test_user):
    res = client.delete("/users/")
    assert res.status_code == 401
