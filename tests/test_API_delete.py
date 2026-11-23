def test_delete_task(client, task_factory):
    task = task_factory()

    response = client.delete(f"/tasks/{task.id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/tasks/{task.id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/999999")

    assert response.status_code == 404
