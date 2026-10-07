from dotenv import load_dotenv

load_dotenv()

from langgraph.types import Command

from backend.graph.graph import graph
from backend.database.postgres import get_engineering_run


def build_initial_state(user_query: str):
    return {
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

        "messages": [],

        "action_required": False,
        "action_type": "none",
        "action_description": "",
        "approval_status": "not_required",
        "action_result": "",

        "run_id": None,
    }


def test_no_approval_required():
    print("\n========================================")
    print("TEST 1: No approval required")
    print("========================================")

    initial_state = build_initial_state(
        "Should I use EC2 or Lambda for a REST API?"
    )

    config = {
        "configurable": {
            "thread_id": "m8-complete-no-approval"
        }
    }

    result = graph.invoke(
        initial_state,
        config,
    )

    print(f"Approval Status: {result['approval_status']}")
    print(f"Action Required: {result['action_required']}")
    print(f"Run ID: {result['run_id']}")

    assert result["approval_status"] == "not_required"
    assert result["action_required"] is False
    assert result["run_id"] is not None

    saved_run = get_engineering_run(result["run_id"])

    assert saved_run is not None
    assert str(saved_run[0]) == result["run_id"]
    assert saved_run[9] is False
    assert saved_run[10] == "none"
    assert saved_run[12] == "not_required"
    assert saved_run[13] == ""

    print("PostgreSQL normal run state verified.")
    print("TEST 1 PASSED")


def test_approval_pending():
    print("\n========================================")
    print("TEST 2: Approval required")
    print("========================================")

    initial_state = build_initial_state(
        "Deploy my RAG application to AWS Lambda."
    )

    config = {
        "configurable": {
            "thread_id": "m8-complete-approve"
        }
    }

    result = graph.invoke(
        initial_state,
        config,
    )

    print(f"Run ID: {result['run_id']}")
    print(f"Approval Status: {result['approval_status']}")
    print(f"Action Type: {result['action_type']}")

    assert result["run_id"] is not None
    assert result["action_required"] is True
    assert result["action_type"] == "deploy"
    assert result["approval_status"] == "pending"

    saved_run = get_engineering_run(result["run_id"])

    assert saved_run is not None
    assert str(saved_run[0]) == str(result["run_id"])
    assert saved_run[9] is True
    assert saved_run[10] == "deploy"
    assert saved_run[12] == "pending"

    print("PostgreSQL pending state verified.")
    print("TEST 2 PASSED")


def test_approval_approved():
    print("\n========================================")
    print("TEST 3: Approval accepted")
    print("========================================")

    config = {
        "configurable": {
            "thread_id": "m8-complete-approve"
        }
    }

    result = graph.invoke(
        Command(resume="approved"),
        config,
    )

    print(f"Run ID: {result['run_id']}")
    print(f"Approval Status: {result['approval_status']}")
    print(f"Action Result: {result['action_result']}")

    assert result["approval_status"] == "approved"
    assert result["action_result"] != ""

    saved_run = get_engineering_run(result["run_id"])

    assert saved_run is not None
    assert str(saved_run[0]) == str(result["run_id"])
    assert saved_run[12] == "approved"
    assert saved_run[13] == result["action_result"]

    print("PostgreSQL approved state verified.")
    print("Action execution verified.")
    print("TEST 3 PASSED")


def test_rejection_pending():
    print("\n========================================")
    print("TEST 4: Destructive action requires approval")
    print("========================================")

    initial_state = build_initial_state(
        "Delete the production EC2 instance."
    )

    config = {
        "configurable": {
            "thread_id": "m8-complete-reject"
        }
    }

    result = graph.invoke(
        initial_state,
        config,
    )

    print(f"Run ID: {result['run_id']}")
    print(f"Approval Status: {result['approval_status']}")
    print(f"Action Type: {result['action_type']}")

    assert result["run_id"] is not None
    assert result["action_required"] is True
    assert result["action_type"] == "delete"
    assert result["approval_status"] == "pending"

    saved_run = get_engineering_run(result["run_id"])

    assert saved_run is not None
    assert str(saved_run[0]) == str(result["run_id"])
    assert saved_run[9] is True
    assert saved_run[10] == "delete"
    assert saved_run[12] == "pending"

    print("PostgreSQL pending state verified.")
    print("TEST 4 PASSED")


def test_rejection_rejected():
    print("\n========================================")
    print("TEST 5: Human rejects action")
    print("========================================")

    config = {
        "configurable": {
            "thread_id": "m8-complete-reject"
        }
    }

    result = graph.invoke(
        Command(resume="rejected"),
        config,
    )

    print(f"Run ID: {result['run_id']}")
    print(f"Approval Status: {result['approval_status']}")
    print(f"Action Result: {result['action_result']}")

    assert result["approval_status"] == "rejected"

    # Action executor should NOT run after rejection.
    assert result["action_result"] == ""

    saved_run = get_engineering_run(result["run_id"])

    assert saved_run is not None
    assert str(saved_run[0]) == str(result["run_id"])
    assert saved_run[12] == "rejected"
    assert saved_run[13] == ""

    print("PostgreSQL rejected state verified.")
    print("Action execution correctly prevented.")
    print("TEST 5 PASSED")


def main():
    test_no_approval_required()
    test_approval_pending()
    test_approval_approved()
    test_rejection_pending()
    test_rejection_rejected()

    print("\n========================================")
    print("ALL M8 HITL TESTS PASSED!")
    print("========================================")


if __name__ == "__main__":
    main()
