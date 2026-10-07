from backend.database.postgres import update_engineering_run
from backend.graph.state import EngineerFlowState


def action_executor(state: EngineerFlowState):
    if not state["action_required"]:
        return {
            "action_result": "No action was required."
        }

    if state["approval_status"] == "rejected":
        return {
            "action_result": "Action rejected by human."
        }

    if state["approval_status"] != "approved":
        raise ValueError(
            "Action cannot be executed without human approval."
        )

    action_type = state["action_type"]
    action_description = state["action_description"]

    result = (
        f"Simulated {action_type} action executed successfully: "
        f"{action_description}"
    )

    update_engineering_run(
        run_id=state["run_id"],
        action_result=result,
    )

    return {
        "action_result": result
    }