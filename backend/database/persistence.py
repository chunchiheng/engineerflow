from backend.database.postgres import (
    create_engineering_run,
    update_engineering_run_analysis,
)
from backend.graph.state import EngineerFlowState


def persist_engineering_run(state: EngineerFlowState):
    """
    Persist an EngineerFlow run to PostgreSQL.

    Synchronous workflow:
        Create a new run.

    Asynchronous workflow:
        Update an existing run.
    """

    run_data = {
        "user_query": state["user_query"],
        "domain": state["domain"],
        "complexity": state["complexity"],
        "selected_agents": state["selected_agents"],
        "cloud_analysis": state["cloud_analysis"],
        "ai_analysis": state["ai_analysis"],
        "systems_analysis": state["systems_analysis"],
        "final_response": state["response"],
        "action_required": state["action_required"],
        "action_type": state["action_type"],
        "action_description": state["action_description"],
        "approval_status": state["approval_status"],
        "action_result": state["action_result"],
    }

    if state["run_id"] is None:
        return create_engineering_run(**run_data)

    run_data.pop("user_query")

    return update_engineering_run_analysis(
        run_id=state["run_id"],
        **run_data,
    )