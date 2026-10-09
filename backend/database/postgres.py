import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set.")

    return psycopg.connect(database_url)


def save_run(
    user_query,
    domain,
    complexity,
    selected_agents,
    cloud_analysis,
    ai_analysis,
    systems_analysis,
    final_response,
    action_required,
    action_type,
    action_description,
    approval_status,
    action_result,
):
    return create_engineering_run(
        user_query=user_query,
        domain=domain,
        complexity=complexity,
        selected_agents=selected_agents,
        cloud_analysis=cloud_analysis,
        ai_analysis=ai_analysis,
        systems_analysis=systems_analysis,
        final_response=final_response,
        action_required=action_required,
        action_type=action_type,
        action_description=action_description,
        approval_status=approval_status,
        action_result=action_result,
    )


def create_engineering_run(
    user_query,
    domain,
    complexity,
    selected_agents,
    cloud_analysis,
    ai_analysis,
    systems_analysis,
    final_response,
    action_required,
    action_type,
    action_description,
    approval_status,
    action_result,
):
    query = """
        INSERT INTO engineering_runs (
            user_query,
            domain,
            complexity,
            selected_agents,
            cloud_analysis,
            ai_analysis,
            systems_analysis,
            final_response,
            action_required,
            action_type,
            action_description,
            approval_status,
            action_result
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        RETURNING id;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    user_query,
                    psycopg.types.json.Json(domain),
                    complexity,
                    psycopg.types.json.Json(selected_agents),
                    cloud_analysis,
                    ai_analysis,
                    systems_analysis,
                    final_response,
                    action_required,
                    action_type,
                    action_description,
                    approval_status,
                    action_result,
                ),
            )

            run_id = cursor.fetchone()[0]

        connection.commit()

    return run_id


def update_engineering_run(
    run_id,
    approval_status=None,
    action_result=None,
):
    query = """
        UPDATE engineering_runs
        SET
            approval_status = COALESCE(%s, approval_status),
            action_result = COALESCE(%s, action_result)
        WHERE id = %s
        RETURNING id;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    approval_status,
                    action_result,
                    run_id,
                ),
            )

            updated_run = cursor.fetchone()

        connection.commit()

    if updated_run is None:
        raise ValueError(
            f"Engineering run not found: {run_id}"
        )

    return updated_run[0]


def get_previous_runs(limit: int = 10):
    query = """
        SELECT
            id,
            user_query,
            domain,
            complexity,
            selected_agents,
            final_response,
            created_at
        FROM engineering_runs
        ORDER BY created_at DESC
        LIMIT %s;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()

    return rows


def get_engineering_run(run_id):
    query = """
        SELECT
            id,
            user_query,
            domain,
            complexity,
            selected_agents,
            cloud_analysis,
            ai_analysis,
            systems_analysis,
            final_response,
            action_required,
            action_type,
            action_description,
            approval_status,
            action_result,
            created_at
        FROM engineering_runs
        WHERE id = %s;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (run_id,))
            row = cursor.fetchone()

    return row


def retrieve_relevant_memories(query_text: str, limit: int = 5):
    query = """
        SELECT
            id,
            user_query,
            domain,
            complexity,
            selected_agents,
            final_response,
            created_at,
            ts_rank(
                to_tsvector(
                    'english',
                    coalesce(user_query, '') || ' ' ||
                    coalesce(final_response, '')
                ),
                websearch_to_tsquery('english', %s)
            ) AS relevance_score
        FROM engineering_runs
        WHERE to_tsvector(
            'english',
            coalesce(user_query, '') || ' ' ||
            coalesce(final_response, '')
        )
        @@ websearch_to_tsquery('english', %s)
        ORDER BY relevance_score DESC, created_at DESC
        LIMIT %s;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (query_text, query_text, limit),
            )
            rows = cursor.fetchall()

    return rows


def update_engineering_run_analysis(
    run_id,
    domain,
    complexity,
    selected_agents,
    cloud_analysis,
    ai_analysis,
    systems_analysis,
    final_response,
    action_required,
    action_type,
    action_description,
    approval_status,
    action_result,
):
    """
    Save LangGraph analysis into an existing engineering run.

    Used by asynchronous tasks that already have a run_id.
    """

    query = """
        UPDATE engineering_runs
        SET
            domain = %s,
            complexity = %s,
            selected_agents = %s,
            cloud_analysis = %s,
            ai_analysis = %s,
            systems_analysis = %s,
            final_response = %s,
            action_required = %s,
            action_type = %s,
            action_description = %s,
            approval_status = %s,
            action_result = %s
        WHERE id = %s
        RETURNING id;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    psycopg.types.json.Json(domain),
                    complexity,
                    psycopg.types.json.Json(selected_agents),
                    cloud_analysis,
                    ai_analysis,
                    systems_analysis,
                    final_response,
                    action_required,
                    action_type,
                    action_description,
                    approval_status,
                    action_result,
                    run_id,
                ),
            )
            row = cursor.fetchone()

    if row is None:
        raise ValueError(
            f"Engineering run not found: {run_id}"
        )

    return row[0]