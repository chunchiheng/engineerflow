from dotenv import load_dotenv

load_dotenv()

from backend.graph.graph import graph


def main():

    initial_state = {
        "user_query": "Deploy my RAG application to AWS Lambda.",

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

        "run_id": None,
    }

    config = {
        "configurable": {
            "thread_id": "m8-persistence-integration-test"
        }
    }

    result = graph.invoke(
        initial_state,
        config,
    )

    print("Workflow paused for human approval.")

    print(f"Run ID: {result['run_id']}")
    print(f"Approval Status: {result['approval_status']}")
    print(f"Action Type: {result['action_type']}")
    print(f"Action Description: {result['action_description']}")

    assert result["run_id"] is not None
    assert result["action_required"] is True
    assert result["approval_status"] == "pending"

    print("\nHITL persistence integration test passed!")


if __name__ == "__main__":
    main()
