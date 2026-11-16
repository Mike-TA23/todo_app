# tests/test_tasks.py
def test_invalid_task_id(client):
    response = client.get("/tasks/not-an-integer")

    assert response.status_code == 422

def test_nonExistant_task_id(client ):
    response = client.get("/tasks/34343")

    assert response.status_code == 404