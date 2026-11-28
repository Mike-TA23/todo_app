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

import pytest


@pytest.mark.parametrize(
    "status",
    ["pending", "in_progress", "completed"],
)
def test_filter_tasks_by_status(client, task_factory, status):
    tasks = {
        value: task_factory(title=value, status=value)
        for value in ["pending", "in_progress", "completed"]
    }

    response = client.get("/tasks/", params={"status": status})

    assert response.status_code == 200
    data = response.json()

    assert [task["id"] for task in data] == [tasks[status].id]
    assert data[0]["status"] == status


def test_filter_with_no_matches(client, task_factory):
    task_factory(status="completed")

    response = client.get("/tasks/", params={"status": "pending"})

    assert response.status_code == 200
    assert response.json() == []


def test_omitting_status_returns_all_statuses(client, task_factory):
    tasks = [
        task_factory(status="pending"),
        task_factory(status="in_progress"),
        task_factory(status="completed"),
    ]

    response = client.get("/tasks/")

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [
        task.id for task in tasks
    ]


@pytest.mark.parametrize("limit", [1, 2, 10])
def test_limit_tasks(client, task_factory, limit):
    tasks = [task_factory(title=f"Task {i}") for i in range(3)]

    response = client.get("/tasks/", params={"limit": limit})

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [
        task.id for task in tasks[:limit]
    ]


def test_limit_applies_to_matching_tasks(client, task_factory):
    task_factory(status="pending")
    first = task_factory(status="completed")
    task_factory(status="in_progress")
    second = task_factory(status="completed")
    task_factory(status="completed")

    response = client.get(
        "/tasks/",
        params={"status": "completed", "limit": 2},
    )

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [
        first.id,
        second.id,
    ]


@pytest.mark.parametrize(
    "parameter, value",
    [
        ("status", "unknown"),
        ("limit", 0),
        ("limit", -1),
        ("limit", 101),
        ("limit", "abc"),
    ],
)
def test_invalid_filter_parameters(client, parameter, value):
    response = client.get("/tasks/", params={parameter: value})

    assert response.status_code == 422
    assert any(
        error["loc"] == ["query", parameter]
        for error in response.json()["detail"]
    )

import pytest


def test_offset_skips_tasks(client, task_factory):
    tasks = [task_factory(title=f"Task {i}") for i in range(5)]

    response = client.get(
        "/tasks/",
        params={"offset": 2, "limit": 2},
    )

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [
        tasks[2].id,
        tasks[3].id,
    ]


def test_offset_defaults_to_zero(client, task_factory):
    tasks = [task_factory(title=f"Task {i}") for i in range(3)]

    response = client.get("/tasks/", params={"limit": 2})

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [
        tasks[0].id,
        tasks[1].id,
    ]


@pytest.mark.parametrize("offset", [3, 10])
def test_offset_at_or_beyond_end_returns_empty_list(
    client, task_factory, offset
):
    for i in range(3):
        task_factory(title=f"Task {i}")

    response = client.get("/tasks/", params={"offset": offset})

    assert response.status_code == 200
    assert response.json() == []


def test_consecutive_pages_have_no_gaps_or_duplicates(client, task_factory):
    tasks = [task_factory(title=f"Task {i}") for i in range(5)]
    returned_ids = []

    for offset in [0, 2, 4]:
        response = client.get(
            "/tasks/",
            params={"offset": offset, "limit": 2},
        )

        assert response.status_code == 200
        page = response.json()
        assert len(page) == min(2, len(tasks) - offset)
        returned_ids.extend(task["id"] for task in page)

    assert returned_ids == [task.id for task in tasks]


def test_offset_applies_after_status_filter(client, task_factory):
    task_factory(status="pending")
    task_factory(status="completed")
    task_factory(status="in_progress")
    expected = task_factory(status="completed")
    task_factory(status="pending")
    task_factory(status="completed")

    response = client.get(
        "/tasks/",
        params={
            "status": "completed",
            "offset": 1,
            "limit": 1,
        },
    )

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [expected.id]


@pytest.mark.parametrize("offset", [-1, "abc", "1.5"])
def test_invalid_offset(client, offset):
    response = client.get("/tasks/", params={"offset": offset})

    assert response.status_code == 422
    assert any(
        error["loc"] == ["query", "offset"]
        for error in response.json()["detail"]
    )