
import time
from uuid import UUID

from backend.database.task_repository import get_task
from backend.worker.tasks import resume_engineering_task


def main():
    print("=== M9.5 HITL Resume Test ===")

    run_id = UUID(
        "787a65a8-96cd-4e19-b556-a27f6eca4cce"
    )

    task = get_task(run_id)

    assert task is not None
    assert task["run_status"] == "awaiting_approval"

    print("[PASS] Original task awaiting approval")

    async_result = resume_engineering_task.delay(
        str(run_id),
        "approved",
    )

    print("[PASS] Resume task submitted")
    print("Resume Celery ID:", async_result.id)

    for _ in range(30):
        task = get_task(run_id)
        status = task["run_status"]

        print("Current status:", status)

        if status == "completed":
            assert task["approval_status"] == "approved"

            print("[PASS] Approval persisted")
            print("[PASS] Workflow resumed")
            print("[PASS] Original run ID preserved")
            print("=== M9.5 Resume Test Passed ===")
            return

        if status == "failed":
            raise AssertionError(
                f"Resume failed: {task['error_message']}"
            )

        time.sleep(2)

    raise TimeoutError(
        "Resume did not finish within 60 seconds."
    )


if __name__ == "__main__":
    main()
