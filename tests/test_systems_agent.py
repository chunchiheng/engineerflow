from dotenv import load_dotenv

load_dotenv()

from backend.agents.systems_agent import systems_agent


state = {
    "user_query": "What are the advantages of Kafka?",
    "domain": "systems",
    "complexity": "medium",
    "key_considerations": [],
    "selected_agents": ["systems"],
    "cloud_analysis": "",
    "ai_analysis": "",
    "systems_analysis": "",
    "response": "",
    "messages": [],
}


result = systems_agent(state)

print("\n=== Systems Agent Analysis ===")
print(result["systems_analysis"])