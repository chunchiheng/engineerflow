from backend.rag.vector_store import get_vector_store


vector_store = get_vector_store()

query = "What are the trade-offs of Kafka?"

results = vector_store.similarity_search(
    query,
    k=3,
)

print("\n=== Query ===")
print(query)

print("\n=== Retrieved Documents ===")

for i, document in enumerate(results):
    print(f"\n--- Result {i + 1} ---")

    print("Content:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)