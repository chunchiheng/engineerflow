from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import SystemMessage, HumanMessage
from backend.graph.graph import graph
from langgraph.types import Command


def main():

    user_query = input("Enter your engineering question: ")

    initial_state = {
        "user_query": user_query,

        "domain": [],
        "complexity": "",
        "key_considerations": [],

        "selected_agents": [],
        "completed_agents": [],

        "cloud_analysis": "",
        "ai_analysis": "",
        "systems_analysis": "",

        "response": "",

        "messages": [
            SystemMessage(
                content="""
    You are EngineerFlow, an AI engineering copilot.

    You help engineers analyze:

    - Cloud Engineering
    - AI Engineering
    - Systems Engineering

    You have access to an engineering knowledge base.

    Use the knowledge base when additional engineering
    information is needed.
    """
            ),
            HumanMessage(
                content=user_query
            ),
        ],

        "action_required": False,
        "action_type": "none",
        "action_description": "",
        "approval_status": "not_required",
        "action_result": "",
        "run_id": None,
    }

    config = {
        "configurable": {
            "thread_id": "main-engineerflow"
        }
    }

    result = graph.invoke(
        initial_state,
        config,
    )

    run_id = result["run_id"]


    if result["action_required"] and result["approval_status"] == "pending":

        print("\n" + "=" * 60)
        print("Human Approval Required")
        print("=" * 60)

        print(f"\nAction Type: {result['action_type']}")
        print(f"Action Description: {result['action_description']}")

        approval = input("\nApprove this action? (yes/no): ").strip().lower()

        if approval == "yes":
            result = graph.invoke(
                Command(resume="approved"),
                config,
            )

        elif approval == "no":
            result = graph.invoke(
                Command(resume="rejected"),
                config,
            )

        else:
            raise ValueError("Please enter 'yes' or 'no'.")

        run_id = result["run_id"]

    print("\n" + "=" * 60)
    print("EngineerFlow")
    print("=" * 60)

    print("\n=== Message History ===")

    for message in result["messages"]:
        print("\n--------------------")
        print("Message type:", type(message).__name__)

        if isinstance(message, dict):
            print("Role:", message["role"])
            print("Content:", message["content"])

        else:
            print("Content:", message.content)

            if hasattr(message, "tool_calls") and message.tool_calls:
                print("Tool calls:", message.tool_calls)

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