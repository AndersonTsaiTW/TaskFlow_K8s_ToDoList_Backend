import os
from pathlib import Path

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_taskflow.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from main import app


TEST_DB_PATH = Path("test_taskflow.db")


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


@pytest.fixture()
def user_payload():
    return {
        "email": "test.user@example.com",
        "name": "Test User",
        "password": "password123",
    }


@pytest.fixture()
def auth_headers(client, user_payload):
    client.post("/api/v1/auth/register", json=user_payload)
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": user_payload["email"],
            "password": user_payload["password"],
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
