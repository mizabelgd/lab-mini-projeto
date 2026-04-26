from fastapi.testclient import TestClient


def test_unauthenticated_request_returns_401(client: TestClient) -> None:
    assert client.get("/tasks").status_code == 401


def test_create_task(client: TestClient, auth_headers: dict) -> None:
    res = client.post("/tasks", json={"title": "Buy milk"}, headers=auth_headers)
    assert res.status_code == 201
    body = res.json()
    assert body["title"] == "Buy milk"
    assert body["status"] == "pending"
    assert body["description"] is None


def test_create_task_with_description(client: TestClient, auth_headers: dict) -> None:
    res = client.post(
        "/tasks",
        json={"title": "Buy milk", "description": "Full fat"},
        headers=auth_headers,
    )
    assert res.status_code == 201
    assert res.json()["description"] == "Full fat"


def test_create_task_empty_title_returns_422(client: TestClient, auth_headers: dict) -> None:
    res = client.post("/tasks", json={"title": "   "}, headers=auth_headers)
    assert res.status_code == 422


def test_list_tasks(client: TestClient, auth_headers: dict) -> None:
    client.post("/tasks", json={"title": "Task A"}, headers=auth_headers)
    client.post("/tasks", json={"title": "Task B"}, headers=auth_headers)
    res = client.get("/tasks", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_list_tasks_filter_pending(client: TestClient, auth_headers: dict) -> None:
    task = client.post("/tasks", json={"title": "A"}, headers=auth_headers).json()
    client.post("/tasks", json={"title": "B"}, headers=auth_headers)
    client.patch(f"/tasks/{task['id']}/complete", headers=auth_headers)

    res = client.get("/tasks?status=pending", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["status"] == "pending"


def test_list_tasks_filter_completed(client: TestClient, auth_headers: dict) -> None:
    task = client.post("/tasks", json={"title": "A"}, headers=auth_headers).json()
    client.post("/tasks", json={"title": "B"}, headers=auth_headers)
    client.patch(f"/tasks/{task['id']}/complete", headers=auth_headers)

    res = client.get("/tasks?status=completed", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["status"] == "completed"


def test_get_task(client: TestClient, auth_headers: dict) -> None:
    task = client.post("/tasks", json={"title": "Test"}, headers=auth_headers).json()
    res = client.get(f"/tasks/{task['id']}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["id"] == task["id"]


def test_get_task_not_found(client: TestClient, auth_headers: dict) -> None:
    assert client.get("/tasks/9999", headers=auth_headers).status_code == 404


def test_update_task(client: TestClient, auth_headers: dict) -> None:
    task = client.post("/tasks", json={"title": "Old"}, headers=auth_headers).json()
    res = client.put(f"/tasks/{task['id']}", json={"title": "New"}, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["title"] == "New"


def test_complete_task(client: TestClient, auth_headers: dict) -> None:
    task = client.post("/tasks", json={"title": "Test"}, headers=auth_headers).json()
    res = client.patch(f"/tasks/{task['id']}/complete", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["status"] == "completed"


def test_complete_already_completed_returns_409(client: TestClient, auth_headers: dict) -> None:
    task = client.post("/tasks", json={"title": "Test"}, headers=auth_headers).json()
    client.patch(f"/tasks/{task['id']}/complete", headers=auth_headers)
    res = client.patch(f"/tasks/{task['id']}/complete", headers=auth_headers)
    assert res.status_code == 409


def test_delete_task(client: TestClient, auth_headers: dict) -> None:
    task = client.post("/tasks", json={"title": "Test"}, headers=auth_headers).json()
    assert client.delete(f"/tasks/{task['id']}", headers=auth_headers).status_code == 204
    assert client.get(f"/tasks/{task['id']}", headers=auth_headers).status_code == 404


def test_task_isolation_between_users(client: TestClient) -> None:
    token_a = client.post(
        "/auth/register", json={"email": "a@x.com", "password": "password123"}
    ).json()["access_token"]
    token_b = client.post(
        "/auth/register", json={"email": "b@x.com", "password": "password123"}
    ).json()["access_token"]

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    task = client.post("/tasks", json={"title": "Private"}, headers=headers_a).json()

    assert client.get(f"/tasks/{task['id']}", headers=headers_b).status_code == 404
    assert client.get("/tasks", headers=headers_b).json() == []
