def task_json(task):
    return {
        "id": task.id,
        "title": task.title,
        "text": task.text,
        "deadline": task.deadline.isoformat(),
        "status": task.status,
    }


def test_read_tasks_when_empty(client):
    response = client.get("/tasks/")

    assert response.status_code == 200
    assert response.json() == []


def test_read_tasks_returns_all_tasks(client, task_factory):
    first = task_factory(title="First task")
    second = task_factory(title="Second task", status="completed")

    response = client.get("/tasks/")

    assert response.status_code == 200
    returned_tasks = {task["id"]: task for task in response.json()}
    assert returned_tasks == {
        first.id: task_json(first),
        second.id: task_json(second),
    }


def test_read_task_by_id(client, task_factory):
    task = task_factory()

    response = client.get(f"/tasks/{task.id}")

    assert response.status_code == 200
    assert response.json() == task_json(task)


def test_invalid_task_id(client):
    response = client.get("/tasks/not-an-integer")

    assert response.status_code == 422


def test_nonexistent_task_id(client):
    response = client.get("/tasks/34343")

    assert response.status_code == 404
    assert response.json() == {"detail": "There is no task with id = 34343"}
