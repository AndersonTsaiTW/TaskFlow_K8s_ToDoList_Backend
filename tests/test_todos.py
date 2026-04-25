def test_create_todo_requires_authentication(client):
    response = client.post("/api/v1/todos", json={"title": "No token"})

    assert response.status_code == 401


def test_authenticated_user_can_manage_todo(client, auth_headers):
    create_response = client.post(
        "/api/v1/todos",
        headers=auth_headers,
        json={
            "title": "Write tests",
            "description": "Cover the TaskFlow API",
            "priority": 3,
            "tags": ["ci", "api"],
        },
    )

    assert create_response.status_code == 201
    todo = create_response.json()
    assert todo["title"] == "Write tests"
    assert todo["status"] == "open"
    assert todo["priority"] == 3

    list_response = client.get("/api/v1/todos", headers=auth_headers)

    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    update_response = client.patch(
        f"/api/v1/todos/{todo['id']}",
        headers=auth_headers,
        json={"status": "done", "title": "Write better tests"},
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["status"] == "done"
    assert updated["title"] == "Write better tests"

    delete_response = client.delete(f"/api/v1/todos/{todo['id']}", headers=auth_headers)

    assert delete_response.status_code == 204

    final_list_response = client.get("/api/v1/todos", headers=auth_headers)

    assert final_list_response.status_code == 200
    assert final_list_response.json()["total"] == 0
