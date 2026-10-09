
import time

from backend.database.task_repository import (
    create_task,
    get_task,
)
from backend.worker.tasks import run_engineering_task


def main():
    print("=== M9.4 Celery LangGraph Test ===")

    user_query = (
        "What are the advantages and disadvantages "
        "of AWS Lambda compared with EC2 for a REST API?"
    )

    run_id = create_task(user_query)

    print("[PASS] Created task:", run_id)

    async_result = run_engineering_task.delay(
        str(run_id)
    )

    print("[PASS] Submitted to Celery")
    print("Celery Task ID:", async_result.id)

    # Allow up to 5 minutes for LLM execution.
    for _ in range(150):
        task = get_task(run_id)

        status = task["run_status"]

        print("Current status:", status)

        if status == "completed":
            assert task["celery_task_id"] == async_result.id
            assert task["final_response"]

            print("\n[PASS] LangGraph completed")
            print("[PASS] Result saved to PostgreSQL")

            print("\n=== Final Response ===")
            print(task["final_response"])

            print("\n=== M9.4 Test Passed ===")
            return

        if status == "awaiting_approval":
            raise AssertionError(
                "Unexpected HITL interruption "
                "for an analysis-only question."
            )

        if status == "failed":
            raise AssertionError(
                f"Worker failed: {task['error_message']}"
            )

        time.sleep(2)

    raise TimeoutError(
        "LangGraph did not finish within 5 minutes."
    )


if __name__ == "__main__":
    main()
