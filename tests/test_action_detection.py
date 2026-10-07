from dotenv import load_dotenv

load_dotenv()

from backend.agents.action_detector import detect_action


def run_test(query: str):
    state = {
        "user_query": query,
    }

    result = detect_action(state)

    print("\n================================")
    print("User Query:")
    print(query)

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

    run_test(
        "What are the advantages of AWS Lambda?"
    )