from backend.database.postgres import get_previous_runs
from backend.graph.graph import graph


def main():

    user_query = "Should I use EC2 or Lambda for a REST API?"

    initial_state = {
        "user_query": user_query,

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

    # Step 1: Run EngineerFlow
    config = {
        "configurable": {
            "thread_id": "m6-persistence-test"
        }
    }

    result = graph.invoke(initial_state, config)

    print("EngineerFlow execution completed.")

    run_id = result["run_id"]

    print("Run persisted by EngineerFlow.")
    print(f"Run ID: {run_id}")

    # Step 3: Load previous runs
    runs = get_previous_runs(limit=10)

    # Step 4: Find the run we just saved
    saved_run = next(
        (run for run in runs if str(run[0]) == str(run_id)),
        None,
    )

    if saved_run is None:
        raise AssertionError(
            "The newly persisted run could not be found in PostgreSQL."
        )

    print("Run retrieved successfully from PostgreSQL.")

    # Validate persisted data
    assert saved_run[1] == user_query
    assert saved_run[2] == result["domain"]
    assert saved_run[3] == result["complexity"]
    assert saved_run[4] == result["selected_agents"]
    assert saved_run[5] == result["response"]

    print("Persisted data matches the LangGraph result.")
    print("\nEnd-to-end persistence test passed!")


if __name__ == "__main__":
    main()