def test_partially_update_task(client, task_factory):
    task = task_factory(
        title="Original title",
        text="Original text",
        deadline="2026-12-01",
        status="pending",
    )

    response = client.patch(
        f"/tasks/{task.id}",
        json={"title": "Updated title", "status": "completed"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": task.id,
        "title": "Updated title",
        "text": "Original text",
        "deadline": "2026-12-01",
        "status": "completed",
    }


def test_partially_update_nonexistent_task(client):
    response = client.patch("/tasks/999999", json={"status": "completed"})

    assert response.status_code == 404


def test_partially_update_task_rejects_invalid_deadline(client, task_factory):
    task = task_factory()

    response = client.patch(
        f"/tasks/{task.id}",
        json={"deadline": "not-a-date"},
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "deadline"]
