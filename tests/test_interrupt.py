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


if __name__ == "__main__":

    state = create_state(
        "Deploy the new RAG application to AWS Lambda."
    )

    config = {
        "configurable": {
            "thread_id": "m8-interrupt-test"
        }
    }

    print("\n=== Starting EngineerFlow ===")

    result = graph.invoke(
        state,
        config=config,
    )

    print("\n=== Graph Paused ===")

    print("Action Required:")
    print(result["action_required"])

    print("Action Type:")
    print(result["action_type"])

    print("Action Description:")
    print(result["action_description"])

    print("Approval Status:")
    print(result["approval_status"])

    print("\n=== Graph State ===")

    snapshot = graph.get_state(config)

    print(snapshot)

    print("\n=== Resume Graph ===")

    result = graph.invoke(
        Command(resume="approved"),
        config=config,
    )

    print("\n=== Graph Resumed ===")

    print("Approval Status:")
    print(result["approval_status"])