
import time

from backend.database.task_repository import (
    create_task,
    get_task,
)
from backend.worker.tasks import run_engineering_task


def main():
    print("=== M9.4 Celery Worker Test ===")

    run_id = create_task(
        "M9.4 Celery Worker integration test"
    )

    print("[PASS] Task created:", run_id)

    async_result = run_engineering_task.delay(
        str(run_id)
    )

    print("[PASS] Task submitted to Redis")
    print("Celery Task ID:", async_result.id)

    for _ in range(30):
        task = get_task(run_id)

        if task["run_status"] == "completed":
            assert task["celery_task_id"] == async_result.id

            print("[PASS] Worker completed task")
            print("[PASS] PostgreSQL status updated")
            print("=== All M9.4 Celery Tests Passed ===")
            return

        if task["run_status"] == "failed":
            raise AssertionError(
                f"Worker failed: {task['error_message']}"
            )

        time.sleep(1)

    raise TimeoutError(
        "Celery Worker did not complete within 30 seconds."
    )


if __name__ == "__main__":
    main()
