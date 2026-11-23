def test_create_task(client, task_payload):
    response = client.post("/tasks/", json=task_payload)

    assert response.status_code == 201
    created = response.json()
    assert isinstance(created["id"], int)
    assert created == {"id": created["id"], **task_payload}
    get_response = client.get(f"/tasks/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == created


def test_create_task_with_missing_required_field(client, task_payload):
    task_payload.pop("title")

    response = client.post("/tasks/", json=task_payload)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]



def test_create_task_with_invalid_deadline(client, task_payload):
    task_payload["deadline"] = "not-a-date"

    response = client.post("/tasks/", json=task_payload)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "deadline"]


def test_create_task_without_optional_field(client, task_payload):
    task_payload.pop("text")

    response = client.post("/tasks/", json=task_payload)

    assert response.status_code == 201
    created = response.json()
    get_response = client.get(f"/tasks/{created['id']}")
    assert get_response.status_code == 200
    assert created == get_response.json()