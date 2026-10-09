
import time

from backend.database.task_repository import (
    create_task,
    get_task,
    update_task_status,
)
from backend.database.postgres import update_engineering_run_analysis
from backend.graph.graph_session import open_graph
from backend.graph.state_factory import create_initial_state
from backend.worker.tasks import resume_engineering_task


def main():
    print("=== M9.5 HITL Rejected Test ===")

    user_query = "Simulated deployment requiring rejection"

    run_id = create_task(user_query)
    run_id_str = str(run_id)

    # Prepare the existing engineering run.
    update_engineering_run_analysis(
        run_id=run_id,
        domain=["cloud"],
        complexity="medium",
        selected_agents=["cloud"],
        cloud_analysis="Simulated cloud analysis",
        ai_analysis="",
        systems_analysis="",
        final_response="Deployment analysis completed.",
        action_required=True,
        action_type="deploy",
        action_description="Simulated deployment",
        approval_status="pending",
        action_result="",
    )

    config = {
        "configurable": {
            "thread_id": run_id_str,
        }
    }

    state = create_initial_state(
        user_query=user_query,
        run_id=run_id_str,
    )

    state.update({
        "action_required": True,
        "action_type": "deploy",
        "action_description": "Simulated deployment",
        "approval_status": "pending",
        "response": "Deployment analysis completed.",
    })

    # Start directly before approval_node, bypassing LLM agents.
    with open_graph() as graph:
        graph.update_state(
            config,
            state,
            as_node="persist_engineering_run",
        )

        result = graph.invoke(None, config=config)
        snapshot = graph.get_state(config)

        assert "approval_node" in snapshot.next
        assert snapshot.interrupts

    update_task_status(run_id, "awaiting_approval")

    print("[PASS] Approval checkpoint prepared")

    async_result = resume_engineering_task.delay(
        run_id_str,
        "rejected",
    )

    print("[PASS] Rejection submitted")
    print("Celery Task ID:", async_result.id)

    for _ in range(30):
        task = get_task(run_id)
        status = task["run_status"]

        if status == "completed":
            assert task["approval_status"] == "rejected"

            action_result = task["action_result"]

            assert action_result in (None, "")

            print("[PASS] Approval rejected")
            print("[PASS] Action Executor skipped")
            print("[PASS] Workflow completed")
            print("=== M9.5 Rejected Test Passed ===")
            return

        if status == "failed":
            raise AssertionError(
                f"Task failed: {task['error_message']}"
            )

        time.sleep(2)

    raise TimeoutError(
        "Rejected workflow did not finish within 60 seconds."
    )


if __name__ == "__main__":
    main()
