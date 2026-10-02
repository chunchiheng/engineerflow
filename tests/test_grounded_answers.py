from dotenv import load_dotenv

load_dotenv()

from backend.graph.graph import graph
from langchain_core.messages import SystemMessage, HumanMessage


def run_test(query: str):
    print("\n" + "=" * 80)
    print("QUERY")
    print("=" * 80)
    print(query)

    initial_state = {
        "user_query": query,
        "domain": "",
        "complexity": "",
        "key_considerations": [],
        "response": "",
        "messages": [
            SystemMessage(
                content="""
        You are EngineerFlow, an AI engineering copilot.

        You help engineers analyze:

        - Cloud Engineering
        - AI Engineering
        - Systems Engineering

        You have access to an engineering knowledge base.

        For questions about engineering concepts that may be
        covered by the knowledge base, you MUST use the
        search_engineering_knowledge tool before answering.

        After receiving the tool result, use the retrieved
        information to provide the final answer.

        Do not answer from your own knowledge when the
        knowledge base can provide relevant information.

        Avoid inventing facts.

        Clearly distinguish assumptions from known information.
        """
            ),
            HumanMessage(
                content=query
            ),
        ],
    }

    result = graph.invoke(initial_state)

    print("\n" + "=" * 80)
    print("FINAL ANSWER")
    print("=" * 80)
    print(result["messages"][-1].content)

    print("\n" + "=" * 80)
    print("RETRIEVED SOURCES")
    print("=" * 80)

    for message in result["messages"]:
        if type(message).__name__ == "ToolMessage":
            print(message.content)


if __name__ == "__main__":

    queries = [
        "What are the disadvantages of AWS Lambda?",
        "What are the differences between RAG and fine-tuning?",
        "What are the advantages of Kafka?",
    ]

    for query in queries:
        run_test(query)