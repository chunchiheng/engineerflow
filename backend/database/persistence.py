from backend.database.postgres import save_run
from backend.graph.state import EngineerFlowState


def persist_engineering_run(state: EngineerFlowState):
    """
    Persist the completed EngineerFlow run to PostgreSQL.
    """

    return save_run(
        user_query=state["user_query"],
        domain=state["domain"],
        complexity=state["complexity"],
        selected_agents=state["selected_agents"],
        cloud_analysis=state["cloud_analysis"],
        ai_analysis=state["ai_analysis"],
        systems_analysis=state["systems_analysis"],
        final_response=state["response"],
    )