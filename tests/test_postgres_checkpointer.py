
from uuid import uuid4

from backend.graph.graph_session import open_graph


def main():
    print("=== M9.5 PostgreSQL Checkpointer Test ===")

    thread_id = str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    # First connection: write a checkpoint.
    with open_graph() as graph:
        graph.update_state(
            config,
            {
                "user_query": "M9.5 checkpoint test",
                "run_id": thread_id,
            },
            as_node="__start__",
        )

        snapshot = graph.get_state(config)

        assert snapshot.values["user_query"] == (
            "M9.5 checkpoint test"
        )

        print("[PASS] Checkpoint written")

    # First connection is now closed.

    # Second connection: read the same checkpoint.
    with open_graph() as graph:
        snapshot = graph.get_state(config)

        assert snapshot.values["user_query"] == (
            "M9.5 checkpoint test"
        )

        assert snapshot.values["run_id"] == thread_id

        print("[PASS] Checkpoint restored")
        print("[PASS] State persisted across connections")

    print("=== M9.5 Checkpointer Test Passed ===")


if __name__ == "__main__":
    main()
