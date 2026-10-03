from dotenv import load_dotenv

load_dotenv()

from backend.agents.cloud_agent import cloud_agent

state = {
    "user_query": "What are the disadvantages of AWS Lambda?",
    "domain": "cloud",
    "complexity": "medium",
    "key_considerations": [],
    "selected_agents": ["cloud"],
    "cloud_analysis": "",
    "ai_analysis": "",
    "systems_analysis": "",
    "response": "",
    "messages": [],
}


result = cloud_agent(state)

print("\n=== Cloud Agent Analysis ===")
print(result["cloud_analysis"])