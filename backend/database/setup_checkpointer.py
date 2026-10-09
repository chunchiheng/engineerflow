
import os

from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver


def main():
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set.")

    print("Initializing PostgreSQL Checkpointer...")

    with PostgresSaver.from_conn_string(
        database_url
    ) as checkpointer:
        checkpointer.setup()

    print("[PASS] PostgreSQL Checkpointer initialized")


if __name__ == "__main__":
    main()
