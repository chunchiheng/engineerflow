from backend.database.postgres import save_run


def main():
    run_id = save_run(
        user_query="Should I use EC2 or Lambda for a REST API?",
        domain=["cloud"],
        complexity="simple",
        selected_agents=["cloud"],
        cloud_analysis="Lambda is suitable for event-driven workloads with variable traffic.",
        ai_analysis="",
        systems_analysis="",
        final_response="For a REST API, Lambda is a strong option when traffic is variable and operational simplicity is important.",
    )

    print("Run saved successfully!")
    print(f"Run ID: {run_id}")


if __name__ == "__main__":
    main()