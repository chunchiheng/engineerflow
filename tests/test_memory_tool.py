from backend.memory.memory_tools import (
    search_previous_engineering_decisions,
)


def main():
    query = "Lambda API"

    result = search_previous_engineering_decisions.invoke(
        {"query": query}
    )

    print("\n" + "=" * 60)
    print("Memory Tool Result")
    print("=" * 60)

    print(result)


if __name__ == "__main__":
    main()