from uuid import uuid4
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.api.main import app


client = TestClient(app)


def make_workflow_state():
    return {
        "selected_agents": [
            "cloud_agent",
            "systems_agent",
        ],
        "completed_agents": [
            "cloud_agent",
        ],
        "next_nodes": [
            "systems_agent",
        ],
        "action_required": True,
        "action_type": "deploy",
        "approval_status": "pending",
        "awaiting_approval": False,
    }


def test_workflow_state_success():
    run_id = uuid4()

    with (
        patch(
            "backend.api.routes.tasks.get_task",
            return_value={
                "run_status": "running",
            },
        ),
        patch(
            "backend.api.routes.tasks.read_workflow_state",
            return_value=make_workflow_state(),
        ),
    ):
        response = client.get(
            f"/api/tasks/{run_id}/state"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["run_id"] == str(run_id)
    assert data["workflow_status"] == "running"
    assert data["selected_agents"] == [
        "cloud_agent",
        "systems_agent",
    ]
    assert data["completed_agents"] == [
        "cloud_agent",
    ]
    assert data["next_nodes"] == [
        "systems_agent",
    ]


def test_workflow_state_awaiting_approval():
    run_id = uuid4()

    workflow = make_workflow_state()
    workflow["next_nodes"] = ["approval_node"]
    workflow["awaiting_approval"] = True

    with (
        patch(
            "backend.api.routes.tasks.get_task",
            return_value={
                "run_status": "awaiting_approval",
            },
        ),
        patch(
            "backend.api.routes.tasks.read_workflow_state",
            return_value=workflow,
        ),
    ):
        response = client.get(
            f"/api/tasks/{run_id}/state"
        )

    assert response.status_code == 200
    assert response.json()["awaiting_approval"] is True
    assert response.json()["approval_status"] == "pending"


def test_workflow_state_not_found():
    run_id = uuid4()

    with patch(
        "backend.api.routes.tasks.get_task",
        return_value=None,
    ):
        response = client.get(
            f"/api/tasks/{run_id}/state"
        )

    assert response.status_code == 404


def test_workflow_state_no_checkpoint():
    run_id = uuid4()

    with (
        patch(
            "backend.api.routes.tasks.get_task",
            return_value={
                "run_status": "queued",
            },
        ),
        patch(
            "backend.api.routes.tasks.read_workflow_state",
            return_value=None,
        ),
    ):
        response = client.get(
            f"/api/tasks/{run_id}/state"
        )

    assert response.status_code == 409


def test_workflow_state_invalid_uuid():
    response = client.get(
        "/api/tasks/invalid-uuid/state"
    )

    assert response.status_code == 422


def test_workflow_state_unavailable():
    run_id = uuid4()

    with (
        patch(
            "backend.api.routes.tasks.get_task",
            return_value={
                "run_status": "running",
            },
        ),
        patch(
            "backend.api.routes.tasks.read_workflow_state",
            side_effect=ConnectionError(
                "Checkpoint database unavailable"
            ),
        ),
    ):
        response = client.get(
            f"/api/tasks/{run_id}/state"
        )

    assert response.status_code == 503
