from backend.agents.approval_node import approval_node


def run_test(
    action_required: bool,
    action_type: str,
    action_description: str,
):
    state = {
        "action_required": action_required,
        "action_type": action_type,
        "action_description": action_description,
        "approval_status": "not_required",
    }

    result = approval_node(state)

    print("\n========================================")
    print("Action Required:")
    print(action_required)

    print("Action Type:")
    print(action_type)

    print("Approval Status:")
    print(result["approval_status"])


if __name__ == "__main__":

    run_test(
        action_required=False,
        action_type="none",
        action_description="No external action required.",
    )

    run_test(
        action_required=True,
        action_type="deploy",
        action_description="Deploy the RAG application to AWS Lambda.",
    )

    run_test(
        action_required=True,
        action_type="delete",
        action_description="Delete the production EC2 instance.",
    )