def test_register_user(client, user_payload):
    response = client.post("/api/v1/auth/register", json=user_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_payload["email"]
    assert data["name"] == user_payload["name"]
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_email_returns_error(client, user_payload):
    client.post("/api/v1/auth/register", json=user_payload)

    response = client.post("/api/v1/auth/register", json=user_payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_returns_bearer_token(client, user_payload):
    client.post("/api/v1/auth/register", json=user_payload)

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": user_payload["email"],
            "password": user_payload["password"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_me_requires_authentication(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_me_returns_current_user(client, user_payload, auth_headers):
    response = client.get("/api/v1/auth/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["email"] == user_payload["email"]
