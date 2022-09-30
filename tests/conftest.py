from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token
from .products import products
import pytest


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}/{settings.database_name}-test"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "testuser@gmail.com",
        "password": "testing123@",
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_admin(client):
    admin_data = {
        "email": "testadmin@gmail.com",
        "password": "admingtesting123@",
        "is_administrator": True,
    }
    res = client.post("/users/", json=admin_data)
    assert res.status_code == 201
    new_admin = res.json()
    new_admin["password"] = admin_data["password"]
    return new_admin


@pytest.fixture
def admin_token(test_admin):
    return create_access_token({"user_id": test_admin["id"]})


@pytest.fixture
def authed_admin_client(client, admin_token):
    client.headers = {**client.headers, "Authorization": f"Bearer {admin_token}"}
    return client


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authed_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def create_multiple_products(authed_admin_client):
    for product in products:
        res = authed_admin_client.post("/products/", json=product)
    assert res.status_code == 201
