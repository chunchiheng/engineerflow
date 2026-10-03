from dotenv import load_dotenv

load_dotenv()

from backend.graph.graph import graph


result = graph.invoke({
    "user_query": "Should I migrate my production RAG application from EC2 to Lambda?",
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
})


print("\n=== Final State ===")
print("Domain:", result["domain"])
print("Complexity:", result["complexity"])
print("Selected Agents:", result["selected_agents"])

print("\n=== Completed Agents ===")
print(result["completed_agents"])

print("\n=== Cloud Analysis ===")
print(repr(result["cloud_analysis"]))

print("\n=== AI Analysis ===")
print(repr(result["ai_analysis"]))

print("\n=== Systems Analysis ===")
print(repr(result["systems_analysis"]))

print("\n=== Final Response ===")
print(result["response"])