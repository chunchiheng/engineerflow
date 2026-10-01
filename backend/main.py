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
    }

    result = graph.invoke(initial_state)

    print("\n" + "=" * 60)
    print("EngineerFlow")
    print("=" * 60)

    print("\nDomain:")
    print(result["domain"])

    print("\nComplexity:")
    print(result["complexity"])

    print("\nKey considerations:")

    for item in result["key_considerations"]:
        print(f"- {item}")

    print("\nAnswer:")
    print(result["response"])


if __name__ == "__main__":
    main()