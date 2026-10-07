from langgraph.types import interrupt

from backend.database.postgres import update_engineering_run
from backend.graph.state import EngineerFlowState


def approval_node(state: EngineerFlowState):
    if not state["action_required"]:
        return {
            "approval_status": "not_required"
        }

    approval_result = interrupt(
        {
            "action_type": state["action_type"],
            "action_description": state["action_description"],
            "message": (
                "Human approval is required before this action "
                "can be executed."
            ),
        }
    )

    if approval_result not in ["approved", "rejected"]:
        raise ValueError(
            "Invalid approval decision. "
            "Expected 'approved' or 'rejected'."
        )

    update_engineering_run(
        run_id=state["run_id"],
        approval_status=approval_result,
    )

    return {
        "approval_status": approval_result
    }
