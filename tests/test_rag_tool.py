from backend.tools.knowledge_tools import search_engineering_knowledge


query = "What are the disadvantages of AWS Lambda?"

result = search_engineering_knowledge.invoke(
    {
        "query": query
    }
)

print("\n=== RAG Tool Result ===")
print(result)