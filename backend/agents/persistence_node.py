from backend.database.persistence import persist_engineering_run
from backend.graph.state import EngineerFlowState


def persist_engineering_run_node(state: EngineerFlowState):
    """
    Persist the current engineering analysis.

    Creates a new run if run_id is None.
    Otherwise updates the existing run.
    """

    run_id = persist_engineering_run(state)

    return {
        "run_id": str(run_id)
    }