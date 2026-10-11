
from uuid import uuid4
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.api.main import app


client = TestClient(app)


def test_approval_success():
    run_id = uuid4()

    with (
        patch(
            "backend.api.routes.tasks.get_task",
            return_value={"id": run_id},
        ),
        patch(
            "backend.api.routes.tasks.claim_task_for_approval",
            return_value=True,
        ),
        patch(
            "backend.api.routes.tasks.resume_engineering_task.delay",
        ) as mock_resume,
    ):
        response = client.post(
            f"/api/tasks/{run_id}/approval",
            json={"decision": "approved"},
        )

    assert response.status_code == 202
    assert response.json() == {
        "run_id": str(run_id),
        "status": "running",
        "decision": "approved",
    }

    mock_resume.assert_called_once_with(
        str(run_id),
        "approved",
        already_claimed=True,
    )


def test_approval_rejected():
    run_id = uuid4()

    with (
        patch(
            "backend.api.routes.tasks.get_task",
            return_value={"id": run_id},
        ),
        patch(
            "backend.api.routes.tasks.claim_task_for_approval",
            return_value=True,
        ),
        patch(
            "backend.api.routes.tasks.resume_engineering_task.delay",
        ) as mock_resume,
    ):
        response = client.post(
            f"/api/tasks/{run_id}/approval",
            json={"decision": "rejected"},
        )

    assert response.status_code == 202

    mock_resume.assert_called_once_with(
        str(run_id),
        "rejected",
        already_claimed=True,
    )


def test_approval_invalid_decision():
    run_id = uuid4()

    response = client.post(
        f"/api/tasks/{run_id}/approval",
        json={"decision": "maybe"},
    )

    assert response.status_code == 422


def test_approval_not_found():
    run_id = uuid4()

    with patch(
        "backend.api.routes.tasks.get_task",
        return_value=None,
    ):
        response = client.post(
            f"/api/tasks/{run_id}/approval",
            json={"decision": "approved"},
        )

    assert response.status_code == 404


def test_approval_duplicate():
    run_id = uuid4()

    with (
        patch(
            "backend.api.routes.tasks.get_task",
            return_value={"id": run_id},
        ),
        patch(
            "backend.api.routes.tasks.claim_task_for_approval",
            return_value=False,
        ),
    ):
        response = client.post(
            f"/api/tasks/{run_id}/approval",
            json={"decision": "approved"},
        )

    assert response.status_code == 409


def test_approval_queue_failure():
    run_id = uuid4()

    with (
        patch(
            "backend.api.routes.tasks.get_task",
            return_value={"id": run_id},
        ),
        patch(
            "backend.api.routes.tasks.claim_task_for_approval",
            return_value=True,
        ),
        patch(
            "backend.api.routes.tasks.resume_engineering_task.delay",
            side_effect=ConnectionError("Redis unavailable"),
        ),
        patch(
            "backend.api.routes.tasks.update_task_status",
        ) as mock_update,
    ):
        response = client.post(
            f"/api/tasks/{run_id}/approval",
            json={"decision": "approved"},
        )

    assert response.status_code == 503

    mock_update.assert_called_once_with(
        run_id,
        "failed",
        error_message="Failed to queue approval task.",
    )
