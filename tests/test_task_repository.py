
from backend.database.task_repository import (
    create_task,
    update_task_status,
    get_task,
)


def main():
    print("=== M9.3 Task Repository Test ===")

    # Test 1: Create task
    run_id = create_task(
        "M9.3 test: Should I use AWS Lambda?"
    )

    task = get_task(run_id)

    assert task is not None
    assert task["run_status"] == "queued"

    print("[PASS] Task created:", run_id)

    # Test 2: Start task
    update_task_status(
        run_id,
        "running",
        celery_task_id="test-celery-task-001",
    )

    task = get_task(run_id)

    assert task["run_status"] == "running"
    assert task["celery_task_id"] == "test-celery-task-001"

    print("[PASS] Task running")

    # Test 3: Complete task
    update_task_status(run_id, "completed")

    task = get_task(run_id)

    assert task["run_status"] == "completed"

    print("[PASS] Task completed")

    # Test 4: Reject invalid status
    try:
        update_task_status(run_id, "unknown")
        raise AssertionError("Invalid status was accepted.")
    except ValueError:
        print("[PASS] Invalid status rejected")

    print("=== All M9.3 Repository Tests Passed ===")


if __name__ == "__main__":
    main()
