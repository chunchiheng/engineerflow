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
    user_query: str,
    domain: list[str],
    complexity: str,
    selected_agents: list[str],
    cloud_analysis: str,
    ai_analysis: str,
    systems_analysis: str,
    final_response: str,
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
            final_response
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
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
                ),
            )

            run_id = cursor.fetchone()[0]

        connection.commit()

    return run_id


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