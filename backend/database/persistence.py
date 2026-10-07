from backend.database.postgres import create_engineering_run
from backend.graph.state import EngineerFlowState


def persist_engineering_run(state: EngineerFlowState):
    """
    Persist a completed EngineerFlow run to PostgreSQL.

    Every engineering run is persisted, regardless of whether
    human approval is required.
    """

    run_id = create_engineering_run(
        user_query=state["user_query"],
        domain=state["domain"],
        complexity=state["complexity"],
        selected_agents=state["selected_agents"],
        cloud_analysis=state["cloud_analysis"],
        ai_analysis=state["ai_analysis"],
        systems_analysis=state["systems_analysis"],
        final_response=state["response"],
        action_required=state["action_required"],
        action_type=state["action_type"],
        action_description=state["action_description"],
        approval_status=state["approval_status"],
        action_result=state["action_result"],
    )

    return run_id

