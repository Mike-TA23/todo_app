def test_replace_task(client, task_factory, task_payload):
    task = task_factory(
        title="Old title",
        text="Old text",
        deadline="2026-11-30",
        status="pending",
    )

    response = client.put(f"/tasks/{task.id}", json=task_payload)

    assert response.status_code == 200
    assert response.json() == {"id": task.id, **task_payload}


def test_replace_nonexistent_task(client, task_payload):
    response = client.put("/tasks/999999", json=task_payload)

    assert response.status_code == 404


def test_replace_task_requires_complete_payload(client, task_factory, task_payload):
    task = task_factory()
    task_payload.pop("status")

    response = client.put(f"/tasks/{task.id}", json=task_payload)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(
        error["loc"] == ["body", "status"]
        and error["type"] == "missing"
        for error in errors
    )
