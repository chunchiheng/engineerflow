from backend.database.postgres import retrieve_relevant_memories


def get_relevant_memories(
    query: str,
    limit: int = 5,
):
    """
    Retrieve relevant previous engineering decisions.

    Args:
        query: Current engineering question.
        limit: Maximum number of memories to retrieve.

    Returns:
        A list of relevant previous engineering runs.
    """
    return retrieve_relevant_memories(
        query_text=query,
        limit=limit,
    )