from dotenv import load_dotenv

load_dotenv()

from backend.graph.graph import graph


def run_test(query: str):
    state = {
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

    result = graph.invoke(state)

    print("\n========================================")
    print("User Query:")
    print(query)

    print("\nFinal Response:")
    print(result["response"])

    print("\nAction Required:")
    print(result["action_required"])

    print("Action Type:")
    print(result["action_type"])

    print("Action Description:")
    print(result["action_description"])

    print("Approval Status:")
    print(result["approval_status"])


if __name__ == "__main__":

    run_test(
        "Should I migrate my production RAG application from EC2 to Lambda?"
    )

    run_test(
        "Deploy the new RAG application to AWS Lambda."
    )

    run_test(
        "Delete the production EC2 instance."
    )