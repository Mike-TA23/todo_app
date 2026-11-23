# tests/test_tasks.py
def test_invalid_task_id(client):
    response = client.get("/tasks/not-an-integer")

    assert response.status_code == 422

def test_nonExistant_task_id(client ):
    response = client.get("/tasks/34343")

    assert response.status_code == 404

def test_create_task(client):
    payload = {
    "title": "string",
    "text": "string",
    "deadline": "2026-11-21",
    "status": "string"
    }

    response = client.post("/tasks/", json=payload)

    assert response.status_code == 201
    created = response.json()
    assert created["title"] == payload["title"]
    assert isinstance(created["id"], int)

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
