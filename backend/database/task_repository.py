
from uuid import UUID

from psycopg.rows import dict_row

from backend.database.postgres import get_connection


VALID_TASK_STATUSES = {
    "queued",
    "running",
    "awaiting_approval",
    "completed",
    "failed",
}


def create_task(user_query: str) -> UUID:
    """Create a queued engineering task and return its run ID."""

    if not user_query or not user_query.strip():
        raise ValueError("user_query cannot be empty.")

    query = """
        INSERT INTO engineering_runs (
            user_query,
            run_status
        )
        VALUES (%s, 'queued')
        RETURNING id;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (user_query,))
            run_id = cursor.fetchone()[0]

    return run_id


def update_task_status(
    run_id: UUID,
    status: str,
    celery_task_id: str | None = None,
    error_message: str | None = None,
) -> UUID:
    """Update the execution status of an existing task."""

    if status not in VALID_TASK_STATUSES:
        raise ValueError(f"Invalid task status: {status}")

    query = """
        UPDATE engineering_runs
        SET
            run_status = %s,
            celery_task_id = COALESCE(%s, celery_task_id),
            error_message = %s
        WHERE id = %s
        RETURNING id;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    status,
                    celery_task_id,
                    error_message,
                    run_id,
                ),
            )
            row = cursor.fetchone()

    if row is None:
        raise ValueError(f"Task not found: {run_id}")

    return row[0]


def get_task(run_id: UUID) -> dict | None:
    query = """
        SELECT
            id,
            user_query,
            run_status,
            celery_task_id,
            error_message,
            approval_status,
            action_result,
            final_response,
            created_at
        FROM engineering_runs
        WHERE id = %s;
    """

    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, (run_id,))
            task = cursor.fetchone()

    return task


def claim_task_for_resume(run_id: UUID) -> bool:
    """
    Atomically claim an awaiting-approval task.

    Only one caller can change its status from
    awaiting_approval to running.
    """

    query = """
        UPDATE engineering_runs
        SET run_status = 'running'
        WHERE id = %s
          AND run_status = 'awaiting_approval'
        RETURNING id;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (run_id,))
            row = cursor.fetchone()

    return row is not None
