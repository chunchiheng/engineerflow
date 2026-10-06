from backend.memory.memory_service import get_relevant_memories


def main():
    query = "Lambda API"

    memories = get_relevant_memories(
        query=query,
        limit=5,
    )

    print(f"Found {len(memories)} relevant memories.")

    for memory in memories:
        run_id = memory[0]
        user_query = memory[1]
        domain = memory[2]
        complexity = memory[3]
        selected_agents = memory[4]
        final_response = memory[5]
        relevance_score = memory[7]

        print("\n" + "=" * 60)
        print(f"Run ID: {run_id}")
        print(f"Question: {user_query}")
        print(f"Domain: {domain}")
        print(f"Complexity: {complexity}")
        print(f"Selected Agents: {selected_agents}")
        print(f"Relevance Score: {relevance_score}")
        print(f"Final Response: {final_response}")


if __name__ == "__main__":
    main()