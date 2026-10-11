
from datetime import datetime, timezone
from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient

from backend.api.main import app


client = TestClient(app)


def make_fake_task(run_id):
    return {
        "id": run_id,
        "user_query": "Design an AWS architecture.",
        "run_status": "completed",
        "celery_task_id": "celery-task-123",
        "final_response": "Use AWS Lambda for bursty workloads.",
        "approval_status": "not_required",
        "action_result": None,
        "error_message": None,
        "created_at": datetime(
            2026, 10, 11, 8, 0,
            tzinfo=timezone.utc,
        ),
    }


def test_get_task_success():
    fake_run_id = uuid4()
    fake_task = make_fake_task(fake_run_id)

    with patch(
        "backend.api.routes.tasks.get_task",
        return_value=fake_task,
    ) as mock_get:
        response = client.get(
            f"/api/tasks/{fake_run_id}"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["run_id"] == str(fake_run_id)
    assert data["status"] == "completed"
    assert data["final_response"] == (
        "Use AWS Lambda for bursty workloads."
    )
    assert data["approval_status"] == "not_required"

    mock_get.assert_called_once_with(fake_run_id)


def test_get_task_not_found():
    fake_run_id = uuid4()

    with patch(
        "backend.api.routes.tasks.get_task",
        return_value=None,
    ):
        response = client.get(
            f"/api/tasks/{fake_run_id}"
        )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Engineering task not found."
    )


def test_get_task_invalid_uuid():
    response = client.get(
        "/api/tasks/not-a-valid-uuid"
    )

    assert response.status_code == 422


def test_get_task_running():
    fake_run_id = uuid4()
    fake_task = make_fake_task(fake_run_id)

    fake_task["run_status"] = "running"
    fake_task["final_response"] = None
    fake_task["approval_status"] = None

    with patch(
        "backend.api.routes.tasks.get_task",
        return_value=fake_task,
    ):
        response = client.get(
            f"/api/tasks/{fake_run_id}"
        )

    assert response.status_code == 200
    assert response.json()["status"] == "running"
    assert response.json()["final_response"] is None


def test_get_task_failed():
    fake_run_id = uuid4()
    fake_task = make_fake_task(fake_run_id)

    fake_task["run_status"] = "failed"
    fake_task["final_response"] = None
    fake_task["error_message"] = "Worker execution failed."

    with patch(
        "backend.api.routes.tasks.get_task",
        return_value=fake_task,
    ):
        response = client.get(
            f"/api/tasks/{fake_run_id}"
        )

    assert response.status_code == 200
    assert response.json()["status"] == "failed"
    assert response.json()["error_message"] == (
        "Worker execution failed."
    )
