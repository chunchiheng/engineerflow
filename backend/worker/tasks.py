
from uuid import UUID

from backend.worker.celery_app import celery_app
from backend.database.task_repository import (
    get_task,
    update_task_status,
)
from backend.graph.state_factory import create_initial_state
from backend.graph.graph_session import open_graph
from langgraph.types import Command
from backend.database.task_repository import claim_task_for_resume

@celery_app.task(
    name="engineerflow.run_engineering_task",
    bind=True,
)
def run_engineering_task(self, run_id: str):
    """
    Execute an EngineerFlow analysis using Celery.

    This stage supports normal asynchronous analysis.

    HITL interruption is detected, but cross-process
    approval/resume is not implemented yet.
    """

    task_uuid = UUID(run_id)

    try:
        task = get_task(task_uuid)

        if task is None:
            raise ValueError(f"Task not found: {run_id}")

        if task["run_status"] != "queued":
            raise ValueError(
                f"Expected queued task, got: {task['run_status']}"
            )

        update_task_status(
            task_uuid,
            "running",
            celery_task_id=self.request.id,
        )

        print(f"[Worker] Starting LangGraph: {run_id}")

        initial_state = create_initial_state(
            user_query=task["user_query"],
            run_id=run_id,
        )

        config = {
            "configurable": {
                "thread_id": run_id,
            }
        }

        with open_graph() as graph:
            result = graph.invoke(
                initial_state,
                config=config,
            )

            snapshot = graph.get_state(config)

        # A paused graph is not a completed workflow.
        if snapshot.next:
            if (
                "approval_node" not in snapshot.next
                or not snapshot.interrupts
            ):
                raise RuntimeError(
                    "Graph paused unexpectedly outside "
                    "the human approval node."
                )

            update_task_status(
                task_uuid,
                "awaiting_approval",
            )

            print(f"[Worker] Graph interrupted: {run_id}")

            return {
                "run_id": run_id,
                "status": "awaiting_approval",
            }

        if result.get("approval_status") == "pending":
            raise RuntimeError(
                "Approval is pending but no graph "
                "interruption was detected."
            )

        update_task_status(
            task_uuid,
            "completed",
        )

        print(f"[Worker] Completed LangGraph: {run_id}")

        return {
            "run_id": run_id,
            "status": "completed",
        }

    except Exception as exc:
        try:
            update_task_status(
                task_uuid,
                "failed",
                error_message=str(exc),
            )
        except Exception:
            # Preserve the original exception.
            pass

        raise


@celery_app.task(
    name="engineerflow.resume_engineering_task",
    bind=True,
)
def resume_engineering_task(
    self,
    run_id: str,
    decision: str,
):
    """
    Resume an interrupted EngineerFlow workflow.

    The PostgreSQL checkpointer restores the
    original LangGraph state.
    """

    if decision not in ("approved", "rejected"):
        raise ValueError(
            "Decision must be 'approved' or 'rejected'."
        )

    task_uuid = UUID(run_id)

    claimed = claim_task_for_resume(task_uuid)

    if not claimed:
        raise ValueError(
            "Task is not awaiting approval or "
            "has already been claimed."
        )

    try:
        config = {
            "configurable": {
                "thread_id": run_id,
            }
        }

        with open_graph() as graph:
            snapshot = graph.get_state(config)

            if (
                "approval_node" not in snapshot.next
                or not snapshot.interrupts
            ):
                raise RuntimeError(
                    "No pending approval interrupt found."
                )

            print(
                f"[Worker] Resuming {run_id}: {decision}"
            )

            result = graph.invoke(
                Command(resume=decision),
                config=config,
            )

            final_snapshot = graph.get_state(config)

        if final_snapshot.next:
            raise RuntimeError(
                "Graph did not finish after approval."
            )

        if result["approval_status"] != decision:
            raise RuntimeError(
                "Approval decision was not persisted "
                "in the graph state."
            )

        update_task_status(
            task_uuid,
            "completed",
        )

        print(
            f"[Worker] Resume completed: {run_id}"
        )

        return {
            "run_id": run_id,
            "status": "completed",
            "approval_status": decision,
            "action_result": result["action_result"],
        }

    except Exception as exc:
        try:
            update_task_status(
                task_uuid,
                "failed",
                error_message=str(exc),
            )
        except Exception:
            pass

        raise
