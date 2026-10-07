from dotenv import load_dotenv

load_dotenv()

from langgraph.types import Command

from backend.graph.graph import graph


def create_state(query: str):
    return {
        "user_query": query,
        "domain": [],
        "complexity": "",
        "key_considerations": [],
        "selected_agents": [],
        "completed_agents": [],
        "cloud_analysis": "",
        "ai_analysis": "",
        "systems_analysis": "",
        "response": "",
        "messages": [],

        "action_required": False,
        "action_type": "none",
        "action_description": "",
        "approval_status": "not_required",
        "action_result": "",
    }


def run_approval_test(decision: str):

    config = {
        "configurable": {
            "thread_id": f"m8-6-{decision}"
        }
    }

    state = create_state(
        "Deploy the new RAG application to AWS Lambda."
    )

    print("\n========================================")
    print(f"Testing decision: {decision}")

    print("\n=== Starting Graph ===")

    result = graph.invoke(
        state,
        config=config,
    )

    print("\n=== Graph Paused ===")

    print("Approval Status:")
    print(result["approval_status"])

    print("\n=== Resuming Graph ===")

    result = graph.invoke(
        Command(resume=decision),
        config=config,
    )

    print("\n=== Graph Finished ===")

    print("Approval Status:")
    print(result["approval_status"])

    print("Action Result:")
    print(result["action_result"])


if __name__ == "__main__":

    run_approval_test("approved")

    run_approval_test("rejected")