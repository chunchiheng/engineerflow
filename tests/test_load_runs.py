from backend.database.postgres import get_previous_runs


def main():
    runs = get_previous_runs(limit=10)

    print(f"Found {len(runs)} previous runs.")

    for run in runs:
        run_id = run[0]
        user_query = run[1]
        domain = run[2]
        complexity = run[3]
        selected_agents = run[4]
        final_response = run[5]
        created_at = run[6]

        print("\n" + "=" * 60)
        print(f"Run ID: {run_id}")
        print(f"Question: {user_query}")
        print(f"Domain: {domain}")
        print(f"Complexity: {complexity}")
        print(f"Selected Agents: {selected_agents}")
        print(f"Created At: {created_at}")
        print(f"Final Response: {final_response}")


if __name__ == "__main__":
    main()