from app import schemas
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
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == email


def test_login_user(client, test_user):
    res = client.post(
        "auth/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
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
        "auth/login",
        data={"username": email, "password": password},
    )
    assert str(res.status_code) == status_code


def test_get_current_authed_user(authed_client_admin):
    res = authed_client_admin.get("/users/")
    user = schemas.UserOut(**res.json())
    assert res.status_code == 200
    assert user.email == "testadmin@gmail.com"


def test_get_user_unauthorized(client):
    res = client.get("/users/")
    assert res.status_code == 401


def test_delete_user(authed_client_admin, test_user):
    res = authed_client_admin.delete("/users/")
    assert res.status_code == 204


def test_delete_user_unauthorized(client, test_user):
    res = client.delete("/users/")
    assert res.status_code == 401
