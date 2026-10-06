from dotenv import load_dotenv

load_dotenv()

from backend.graph.graph import graph
from backend.database.persistence import persist_engineering_run


state = {
    "user_query": "What did EngineerFlow previously recommend for using EC2 or Lambda for a REST API?",
    "domain": [],
    "complexity": "",
    "key_considerations": [],
    "selected_agents": [],
    "completed_agents": [],
    "cloud_analysis": "",
    "ai_analysis": "",
    "systems_analysis": "",
    "response": "",
    "messages": [],
}


print("\n=== Running EngineerFlow Memory Integration Test ===")

result = graph.invoke(state)


print("\n=== Supervisor Result ===")
print("Domain:", result["domain"])
print("Complexity:", result["complexity"])
print("Selected Agents:", result["selected_agents"])


print("\n=== Cloud Analysis ===")
print(result["cloud_analysis"])


print("\n=== AI Analysis ===")
print(result["ai_analysis"])


print("\n=== Systems Analysis ===")
print(result["systems_analysis"])


print("\n=== Final Response ===")
print(result["response"])