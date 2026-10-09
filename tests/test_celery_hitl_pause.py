
import time

from backend.database.task_repository import (
    create_task,
    get_task,
)
from backend.worker.tasks import run_engineering_task
from backend.graph.graph_session import open_graph


def main():
    print("=== M9.5 Celery HITL Pause Test ===")

    user_query = (
        "Deploy my RAG application to AWS Lambda. "
        "Analyze the architecture first and request "
        "human approval before deployment."
    )

    run_id = create_task(user_query)

    print("[PASS] Task created:", run_id)

    async_result = run_engineering_task.delay(
        str(run_id)
    )

    print("[PASS] Submitted to Celery")
    print("Celery Task ID:", async_result.id)

    for _ in range(150):
        task = get_task(run_id)
        status = task["run_status"]

        print("Current status:", status)

        if status == "awaiting_approval":
            assert task["celery_task_id"] == async_result.id
            assert task["action_required"] if "action_required" in task else True

            config = {
                "configurable": {
                    "thread_id": str(run_id),
                }
            }

            with open_graph() as graph:
                snapshot = graph.get_state(config)

            assert "approval_node" in snapshot.next
            assert snapshot.interrupts

            print("[PASS] HITL interrupt detected")
            print("[PASS] PostgreSQL status: awaiting_approval")
            print("[PASS] Checkpoint persisted")

            print("=== M9.5 HITL Pause Test Passed ===")
            return

        if status == "failed":
            raise AssertionError(
                f"Worker failed: {task['error_message']}"
            )

        if status == "completed":
            raise AssertionError(
                "Expected HITL pause, but task completed."
            )

        time.sleep(2)

    raise TimeoutError(
        "HITL task did not pause within 5 minutes."
    )


if __name__ == "__main__":
    main()
