from langchain_core.tools import tool

from backend.memory.memory_service import get_relevant_memories


@tool
def search_previous_engineering_decisions(query: str) -> str:
    """
    Search previous EngineerFlow engineering decisions
    that are relevant to the current question.

    Use this tool when previous engineering decisions,
    recommendations, or similar problems may provide
    useful context.
    """

    memories = get_relevant_memories(
        query=query,
        limit=5,
    )

    if not memories:
        return "No relevant previous engineering decisions were found."

    formatted_memories = []

    for i, memory in enumerate(memories):
        run_id = memory[0]
        user_query = memory[1]
        domain = memory[2]
        complexity = memory[3]
        selected_agents = memory[4]
        final_response = memory[5]
        created_at = memory[6]
        relevance_score = memory[7]

        formatted_memories.append(
            f"""
--- Previous Decision {i + 1} ---

Run ID:
{run_id}

Original Question:
{user_query}

Domain:
{domain}

Complexity:
{complexity}

Selected Agents:
{selected_agents}

Final Response:
{final_response}

Relevance Score:
{relevance_score}

Created At:
{created_at}
""".strip()
        )

    return "\n\n".join(formatted_memories)