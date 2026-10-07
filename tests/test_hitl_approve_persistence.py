from dotenv import load_dotenv

load_dotenv()

from langgraph.types import Command

from backend.graph.graph import graph
from backend.database.postgres import get_engineering_run


def main():

    initial_state = {
        "user_query": "Deploy my RAG application to AWS Lambda.",

        "domain": [],
        "complexity": "",
        "key_considerations": [],

        "selected_agents": [],
        "completed_agents": [],

        "cloud_analysis": "",
        "ai_analysis": "",
        "systems_analysis": "",

        "response": "",

        "messages": [],

        "action_required": False,
        "action_type": "none",
        "action_description": "",
        "approval_status": "not_required",
        "action_result": "",

        "run_id": None,
    }

    config = {
        "configurable": {
            "thread_id": "m8-approve-persistence-test"
        }
    }

    # --------------------------------------------------
    # Step 1: Start workflow
    # --------------------------------------------------

    pending_result = graph.invoke(
        initial_state,
        config,
    )

    print("Workflow paused for approval.")

    run_id = pending_result["run_id"]

    print(f"Run ID: {run_id}")
    print(
        f"Approval Status: "
        f"{pending_result['approval_status']}"
    )

    assert run_id is not None
    assert pending_result["approval_status"] == "pending"

    # --------------------------------------------------
    # Step 2: Resume workflow with approval
    # --------------------------------------------------

    approved_result = graph.invoke(
        Command(resume="approved"),
        config,
    )

    print("\nWorkflow resumed after approval.")

    print(
        f"Approval Status: "
        f"{approved_result['approval_status']}"
    )

    print(
        f"Action Result: "
        f"{approved_result['action_result']}"
    )

    # --------------------------------------------------
    # Step 3: Validate LangGraph state
    # --------------------------------------------------

    assert approved_result["run_id"] == run_id

    assert approved_result["approval_status"] == "approved"

    assert approved_result["action_result"] != ""

    print("\nLangGraph state verification passed.")

    # --------------------------------------------------
    # Step 4: Load the same run from PostgreSQL
    # --------------------------------------------------

    saved_run = get_engineering_run(run_id)

    assert saved_run is not None

    print("\nRun retrieved from PostgreSQL.")

    # Database column positions:
    #
    # 0  id
    # 1  user_query
    # 2  domain
    # 3  complexity
    # 4  selected_agents
    # 5  cloud_analysis
    # 6  ai_analysis
    # 7  systems_analysis
    # 8  final_response
    # 9  action_required
    # 10 action_type
    # 11 action_description
    # 12 approval_status
    # 13 action_result
    # 14 created_at

    assert str(saved_run[0]) == str(run_id)

    assert saved_run[9] is True

    assert saved_run[10] == "deploy"

    assert saved_run[12] == "approved"

    assert saved_run[13] == approved_result["action_result"]

    # --------------------------------------------------
    # Step 5: Final verification
    # --------------------------------------------------

    print(f"Database Run ID: {saved_run[0]}")
    print(f"Database Approval Status: {saved_run[12]}")
    print(f"Database Action Result: {saved_run[13]}")

    print("\nHITL approval persistence test passed!")


if __name__ == "__main__":
    main()
