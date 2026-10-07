from backend.database.persistence import persist_engineering_run
from backend.graph.state import EngineerFlowState


def persist_engineering_run_node(state: EngineerFlowState):
    """
    Persist every EngineerFlow run to PostgreSQL.

    This node creates exactly one engineering_runs record
    for the current workflow execution.

    HITL runs are persisted with approval_status='pending',
    while normal engineering runs are persisted with
    approval_status='not_required'.
    """

    if state["run_id"] is not None:
        return {}

    run_id = persist_engineering_run(state)

    return {
        "run_id": str(run_id)
    }

