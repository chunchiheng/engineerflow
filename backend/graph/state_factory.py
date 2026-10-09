
from langchain_core.messages import SystemMessage, HumanMessage


SYSTEM_PROMPT = """
You are EngineerFlow, an AI engineering copilot.

You help engineers analyze:
- Cloud Engineering
- AI Engineering
- Systems Engineering

You have access to an engineering knowledge base.

Use the knowledge base when additional engineering
information is needed.
"""


def create_initial_state(
    user_query: str,
    run_id: str | None = None,
):
    return {
        "user_query": user_query,
        "domain": [],
        "complexity": "",
        "key_considerations": [],
        "selected_agents": [],
        "completed_agents": [],
        "cloud_analysis": "",
        "ai_analysis": "",
        "systems_analysis": "",
        "response": "",
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_query),
        ],
        "action_required": False,
        "action_type": "none",
        "action_description": "",
        "approval_status": "not_required",
        "action_result": "",
        "run_id": run_id,
    }
