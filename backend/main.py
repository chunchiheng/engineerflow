from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import SystemMessage, HumanMessage

from backend.graph.graph import graph


def main():

    user_query = input("Enter your engineering question: ")

    initial_state = {
        "user_query": user_query,
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

    Use the knowledge base when additional engineering
    information is needed.
    """
            ),
            HumanMessage(
                content=user_query
            ),
        ],
    }

    result = graph.invoke(initial_state)

    print("\n" + "=" * 60)
    print("EngineerFlow")
    print("=" * 60)

    print("\n=== Message History ===")

    for message in result["messages"]:
        print("\n--------------------")
        print("Message type:", type(message).__name__)

        if isinstance(message, dict):
            print("Role:", message["role"])
            print("Content:", message["content"])

        else:
            print("Content:", message.content)

            if hasattr(message, "tool_calls") and message.tool_calls:
                print("Tool calls:", message.tool_calls)


if __name__ == "__main__":
    main()