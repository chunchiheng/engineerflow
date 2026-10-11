from uuid import UUID

from backend.graph.graph_session import open_graph


def read_workflow_state(run_id: UUID) -> dict | None:
    config = {
        "configurable": {
            "thread_id": str(run_id),
        }
    }

    with open_graph() as graph:
        snapshot = graph.get_state(config)

    # No checkpoint exists for this run yet.
    if not snapshot or not snapshot.values:
        return None

    values = snapshot.values

    return {
        "selected_agents": list(
            values.get("selected_agents") or []
        ),
        "completed_agents": list(
            values.get("completed_agents") or []
        ),
        "next_nodes": list(snapshot.next or []),
        "action_required": bool(
            values.get("action_required", False)
        ),
        "action_type": values.get("action_type"),
        "approval_status": values.get("approval_status"),
        "awaiting_approval": bool(
            snapshot.interrupts
        ),
    }
