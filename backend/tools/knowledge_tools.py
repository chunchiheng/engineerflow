from langchain_core.tools import tool

from backend.rag.vector_store import get_vector_store


@tool
def search_engineering_knowledge(query: str) -> str:
    """
    Search the EngineerFlow engineering knowledge base
    using semantic similarity search.

    Use this tool when additional engineering knowledge
    is needed to answer the user's question.
    """

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        query,
        k=3,
    )

    if not results:
        return "No relevant engineering knowledge was found."

    formatted_results = []

    for i, document in enumerate(results):
        formatted_results.append(
            f"""
--- Result {i + 1} ---

Content:
{document.page_content}

Metadata:
{document.metadata}
""".strip()
        )

    return "\n\n".join(formatted_results)