from dotenv import load_dotenv

load_dotenv()

from backend.agents.ai_agent import ai_agent


state = {
    "user_query": "What are the differences between RAG and fine-tuning?",
    "domain": "ai",
    "complexity": "medium",
    "key_considerations": [],
    "selected_agents": ["ai"],
    "cloud_analysis": "",
    "ai_analysis": "",
    "systems_analysis": "",
    "response": "",
    "messages": [],
}


result = ai_agent(state)

print("\n=== AI Agent Analysis ===")
print(result["ai_analysis"])