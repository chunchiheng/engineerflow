from dotenv import load_dotenv

load_dotenv()

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
            {
                "role": "system",
                "content": """
You are EngineerFlow, an AI engineering copilot.

You help engineers analyze:

- Cloud Engineering
- AI Engineering
- Systems Engineering

You have access to an engineering knowledge base.

Use the knowledge base when additional engineering
information is needed.
"""
            },
            {
                "role": "user",
                "content": user_query,
            },
        ],
    }

    result = graph.invoke(initial_state)

    print("\n" + "=" * 60)
    print("EngineerFlow")
    print("=" * 60)

    print("\nAnswer:")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()