from backend.database.postgres import (
    create_engineering_run,
    update_engineering_run,
)


def main():

    # Step 1: Create a pending engineering run
    run_id = create_engineering_run(
        user_query="Deploy my RAG application to AWS Lambda.",
        domain=["cloud", "ai"],
        complexity="medium",
        selected_agents=["cloud_agent", "ai_agent"],
        cloud_analysis="Lambda provides serverless deployment.",
        ai_analysis="The RAG application may require external state.",
        systems_analysis="Cold starts and connection management should be considered.",
        final_response="Lambda may be suitable, but deployment requires approval.",
        action_required=True,
        action_type="deploy",
        action_description="Deploy the RAG application to AWS Lambda.",
        approval_status="pending",
        action_result="",
    )

    print("Engineering run created.")
    print(f"Run ID: {run_id}")

    # Step 2: Approve the action
    updated_run_id = update_engineering_run(
        run_id=run_id,
        approval_status="approved",
    )

    print("Approval status updated.")
    print(f"Updated Run ID: {updated_run_id}")

    # The same database record must be updated
    assert str(updated_run_id) == str(run_id)

    # Step 3: Store the action result
    final_run_id = update_engineering_run(
        run_id=run_id,
        action_result=(
            "Simulated deploy action executed successfully: "
            "Deploy the RAG application to AWS Lambda."
        ),
    )

    print("Action result updated.")
    print(f"Final Run ID: {final_run_id}")

    # Again, the same record must be updated
    assert str(final_run_id) == str(run_id)

    print("\nHITL persistence API test passed!")


if __name__ == "__main__":
    main()
