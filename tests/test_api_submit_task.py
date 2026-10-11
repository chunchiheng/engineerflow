
from uuid import uuid4
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.api.main import app


client = TestClient(app)


def test_submit_task_success():
    fake_run_id = uuid4()

    with (
        patch(
            "backend.api.routes.tasks.create_task",
            return_value=fake_run_id,
        ) as mock_create,
        patch(
            "backend.api.routes.tasks.run_engineering_task.delay",
        ) as mock_delay,
    ):
        response = client.post(
            "/api/tasks",
            json={
                "user_query": "Design a scalable RAG system."
            },
        )

    assert response.status_code == 202

    assert response.json() == {
        "run_id": str(fake_run_id),
        "status": "queued",
    }

    mock_create.assert_called_once_with(
        "Design a scalable RAG system."
    )

    mock_delay.assert_called_once_with(
        str(fake_run_id)
    )


def test_submit_task_empty_query():
    response = client.post(
        "/api/tasks",
        json={"user_query": "   "},
    )

    assert response.status_code == 422


def test_submit_task_missing_query():
    response = client.post(
        "/api/tasks",
        json={},
    )

    assert response.status_code == 422


def test_submit_task_queue_failure():
    fake_run_id = uuid4()

    with (
        patch(
            "backend.api.routes.tasks.create_task",
            return_value=fake_run_id,
        ),
        patch(
            "backend.api.routes.tasks.run_engineering_task.delay",
            side_effect=ConnectionError("Redis unavailable"),
        ),
        patch(
            "backend.api.routes.tasks.update_task_status",
        ) as mock_update,
    ):
        response = client.post(
            "/api/tasks",
            json={
                "user_query": "Design an AWS architecture."
            },
        )

    assert response.status_code == 503

    mock_update.assert_called_once_with(
        fake_run_id,
        "failed",
        error_message="Failed to submit task to queue.",
    )
