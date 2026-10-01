from langchain_core.tools import tool


ENGINEERING_KNOWLEDGE = {
    "lambda": """
AWS Lambda is a serverless compute service.

Lambda runs code without requiring users to manage servers.
It is commonly used for event-driven workloads, APIs,
background processing, and applications with variable traffic.

Important considerations include execution duration,
concurrency, cold starts, memory allocation, and cost.
""",

    "ec2": """
Amazon EC2 provides virtual servers in the AWS cloud.

EC2 gives engineers more control over the operating system,
runtime environment, networking, storage, and compute resources.

Important considerations include instance sizing,
autoscaling, patching, availability, and infrastructure cost.
""",

    "rag": """
Retrieval-Augmented Generation (RAG) combines information
retrieval with a language model.

A typical RAG system retrieves relevant documents from a
knowledge base and provides them to an LLM as context
before generating an answer.

RAG is useful when information changes frequently or when
answers should be grounded in external documents.
""",

    "fine-tuning": """
Fine-tuning adapts a pretrained model using additional
training data for a specific task or behavior.

Fine-tuning can be useful for improving task-specific
behavior, formatting, or domain-specific patterns.

It is different from RAG because the model parameters
are updated during fine-tuning, while RAG provides
external information as context at inference time.
""",
}


@tool
def search_engineering_knowledge(query: str) -> str:
    """
    Search the EngineerFlow engineering knowledge base.

    Use this tool when additional engineering knowledge
    is needed to answer the user's question.
    """

    query_lower = query.lower()

    results = []

    for topic, knowledge in ENGINEERING_KNOWLEDGE.items():
        if topic in query_lower:
            results.append(
                f"### {topic}\n{knowledge.strip()}"
            )

    if not results:
        return "No relevant engineering knowledge was found."

    return "\n\n".join(results)