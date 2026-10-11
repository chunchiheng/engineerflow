
from fastapi import APIRouter, HTTPException, status

from backend.api.schemas import (
    TaskCreateRequest,
    TaskCreateResponse,
    TaskStatusResponse,
    TaskApprovalRequest,
    TaskApprovalResponse,
)
from backend.database.task_repository import (
    create_task,
    update_task_status,
    get_task,
    claim_task_for_approval,
)
from backend.worker.tasks import (
    run_engineering_task,
    resume_engineering_task,
)


router = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"],
)


@router.post(
    "",
    response_model=TaskCreateResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def submit_engineering_task(
    request: TaskCreateRequest,
):
    # Step 1: Create a queued task in PostgreSQL.
    run_id = create_task(request.user_query)

    # Step 2: Submit the task to Celery.
    try:
        run_engineering_task.delay(str(run_id))

    except Exception as exc:
        # Avoid leaving a permanently queued record
        # if publishing to Redis fails.
        update_task_status(
            run_id,
            "failed",
            error_message="Failed to submit task to queue.",
        )

        raise HTTPException(
            status_code=503,
            detail="Task queue is temporarily unavailable.",
        ) from exc

    # Step 3: Return immediately.
    return TaskCreateResponse(
        run_id=run_id,
        status="queued",
    )



from uuid import UUID


@router.get(
    "/{run_id}",
    response_model=TaskStatusResponse,
)
def get_engineering_task(run_id: UUID):
    task = get_task(run_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engineering task not found.",
        )

    return TaskStatusResponse(
        run_id=task["id"],
        status=task["run_status"],
        user_query=task["user_query"],
        celery_task_id=task["celery_task_id"],
        final_response=task["final_response"],
        approval_status=task["approval_status"],
        action_result=task["action_result"],
        error_message=task["error_message"],
        created_at=task["created_at"],
    )


@router.post(
    "/{run_id}/approval",
    response_model=TaskApprovalResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def approve_engineering_task(
    run_id: UUID,
    request: TaskApprovalRequest,
):
    task = get_task(run_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Engineering task not found.",
        )

    claimed = claim_task_for_approval(run_id)

    if not claimed:
        raise HTTPException(
            status_code=409,
            detail=(
                "Task is not awaiting approval "
                "or approval has already been submitted."
            ),
        )

    try:
        resume_engineering_task.delay(
            str(run_id),
            request.decision,
            already_claimed=True,
        )

    except Exception as exc:
        update_task_status(
            run_id,
            "failed",
            error_message="Failed to queue approval task.",
        )

        raise HTTPException(
            status_code=503,
            detail="Task queue is temporarily unavailable.",
        ) from exc

    return TaskApprovalResponse(
        run_id=run_id,
        status="running",
        decision=request.decision,
    )
