
from uuid import uuid4

from dotenv import load_dotenv
from langgraph.types import Command

from backend.graph.graph_session import open_graph
from backend.graph.state_factory import create_initial_state


load_dotenv()


def main():
    user_query = input(
        "Enter your engineering question: "
    )

    initial_state = create_initial_state(
        user_query=user_query,
        run_id=None,
    )

    # Use a unique thread for every CLI execution.
    thread_id = str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    with open_graph() as graph:

        result = graph.invoke(
            initial_state,
            config,
        )

        snapshot = graph.get_state(config)

        if snapshot.next:
            print("\n" + "=" * 60)
            print("Human Approval Required")
            print("=" * 60)

            print(
                f"\nAction Type: {result['action_type']}"
            )
            print(
                f"Action Description: "
                f"{result['action_description']}"
            )

            approval = input(
                "\nApprove this action? (yes/no): "
            ).strip().lower()

            if approval == "yes":
                decision = "approved"
            elif approval == "no":
                decision = "rejected"
            else:
                raise ValueError(
                    "Please enter 'yes' or 'no'."
                )

            result = graph.invoke(
                Command(resume=decision),
                config,
            )

        run_id = result["run_id"]

    print("\n" + "=" * 60)
    print("EngineerFlow")
    print("=" * 60)

    print("\n=== Message History ===")

    for message in result["messages"]:
        print("\n--------------------")
        print(
            "Message type:",
            type(message).__name__,
        )

        if isinstance(message, dict):
            print("Role:", message["role"])
            print("Content:", message["content"])
        else:
            print("Content:", message.content)

            if (
                hasattr(message, "tool_calls")
                and message.tool_calls
            ):
                print(
                    "Tool calls:",
                    message.tool_calls,
                )

    print("\nRun saved to PostgreSQL.")

    print("\n=== Final Response ===")
    print(result["response"])

    if result["action_required"]:
        print("\n=== Action Result ===")
        print(result["action_result"])

    print("\n=== Approval Status ===")
    print(result["approval_status"])

    print(f"Run ID: {run_id}")


if __name__ == "__main__":
    main()
