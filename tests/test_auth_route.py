from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.database.database import get_db
from app.dependencies.user_validate import get_current_user
from app.routes import auth_route


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(auth_route.router)
    app.dependency_overrides[get_db] = lambda: None

    with TestClient(app) as test_client:
        yield test_client


def test_create_user(client, monkeypatch):
    monkeypatch.setattr(auth_route.AuthService, "create_user", lambda self, user: None)

    response = client.post(
        "/auth/create",
        json={"username": "alice", "email": "alice@example.com", "password": "secret"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Created successfully !!"}


def test_login(client, monkeypatch):
    monkeypatch.setattr(
        auth_route.AuthService, "login_user", lambda self, email, password: "test-token"
    )

    response = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "secret"},
    )

    assert response.status_code == 200
    assert response.json() == {"id": "user_object.id", "token": "test-token"}


def test_secure_endpoint(client):
    client.app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        username="alice"
    )

    response = client.get("/auth/secure")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Access granted",
        "user": "alice",
        "data": "This is confidential information",
    }
