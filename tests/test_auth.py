from fastapi.testclient import TestClient


def test_register_returns_token(client: TestClient) -> None:
    res = client.post("/auth/register", json={"email": "a@b.com", "password": "password123"})
    assert res.status_code == 201
    body = res.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_register_duplicate_email_returns_409(client: TestClient) -> None:
    payload = {"email": "a@b.com", "password": "password123"}
    client.post("/auth/register", json=payload)
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 409


def test_register_invalid_email_returns_422(client: TestClient) -> None:
    res = client.post("/auth/register", json={"email": "not-an-email", "password": "password123"})
    assert res.status_code == 422


def test_register_short_password_returns_422(client: TestClient) -> None:
    res = client.post("/auth/register", json={"email": "a@b.com", "password": "short"})
    assert res.status_code == 422


def test_login_returns_token(client: TestClient) -> None:
    client.post("/auth/register", json={"email": "a@b.com", "password": "password123"})
    res = client.post("/auth/login", json={"email": "a@b.com", "password": "password123"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_wrong_password_returns_401(client: TestClient) -> None:
    client.post("/auth/register", json={"email": "a@b.com", "password": "password123"})
    res = client.post("/auth/login", json={"email": "a@b.com", "password": "wrongpass"})
    assert res.status_code == 401


def test_login_nonexistent_user_returns_401(client: TestClient) -> None:
    res = client.post("/auth/login", json={"email": "ghost@b.com", "password": "password123"})
    assert res.status_code == 401
