from backend.database.task_repository import (
    create_task,
    get_task,
)
from backend.database.persistence import persist_engineering_run
from backend.database.postgres import get_engineering_run


def make_state(run_id):
    return {
        "user_query": "M9.3 persistence integration test",
        "domain": ["cloud"],
        "complexity": "medium",
        "selected_agents": ["cloud"],
        "cloud_analysis": "AWS Lambda is suitable for event-driven workloads.",
        "ai_analysis": "",
        "systems_analysis": "",
        "response": "Consider Lambda for variable traffic.",
        "action_required": False,
        "action_type": "none",
        "action_description": "",
        "approval_status": "not_required",
        "action_result": "",
        "run_id": run_id,
    }


def main():
    print("=== M9.3 Async Persistence Test ===")

    run_id = create_task(
        "M9.3 persistence integration test"
    )

    print("[PASS] Created queued task:", run_id)

    state = make_state(str(run_id))

    persisted_id = persist_engineering_run(state)

    assert str(persisted_id) == str(run_id)

    print("[PASS] Updated existing run")

    task = get_task(run_id)

    assert task["run_status"] == "queued"
    assert task["final_response"] == (
        "Consider Lambda for variable traffic."
    )

    print("[PASS] Analysis saved to same run")

    saved_run = get_engineering_run(run_id)

    assert saved_run is not None
    assert str(saved_run[0]) == str(run_id)

    print("[PASS] Run ID unchanged")

    # Test legacy synchronous persistence.
    sync_state = make_state(None)

    sync_run_id = persist_engineering_run(sync_state)

    assert sync_run_id is not None

    print("[PASS] Synchronous INSERT still works")

    print("=== All M9.3 Persistence Tests Passed ===")


if __name__ == "__main__":
    main()