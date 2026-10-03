from dotenv import load_dotenv

load_dotenv()

from backend.agents.supervisor import supervisor_agent


state = {
    "user_query": "Should I migrate my production RAG application from EC2 to Lambda?",
    "domain": "",
    "complexity": "",
    "key_considerations": [],
    "selected_agents": [],
    "cloud_analysis": "",
    "ai_analysis": "",
    "systems_analysis": "",
    "response": "",
    "messages": [],
}


result = supervisor_agent(state)

print("\n=== Supervisor Decision ===")
print("Domain:", result["domain"])
print("Complexity:", result["complexity"])
print("Selected Agents:", result["selected_agents"])