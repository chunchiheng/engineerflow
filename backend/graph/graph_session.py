
import os
from contextlib import contextmanager

from dotenv import load_dotenv

# Load environment variables BEFORE importing graph modules.
load_dotenv()

from langgraph.checkpoint.postgres import PostgresSaver
from backend.graph.graph import build_graph


@contextmanager
def open_graph():
    """
    Open a LangGraph instance backed by PostgreSQL.

    Keep the checkpoint connection open during
    graph execution and state inspection.
    """

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set.")

    with PostgresSaver.from_conn_string(
        database_url
    ) as checkpointer:

        graph = build_graph(checkpointer)

        yield graph
