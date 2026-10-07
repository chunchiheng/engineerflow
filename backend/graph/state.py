from typing import TypedDict, Any, Annotated
from operator import add

from langgraph.graph.message import add_messages


class EngineerFlowState(TypedDict):
    user_query: str

    domain: list[str]
    complexity: str
    key_considerations: list[str]

    selected_agents: list[str]
    completed_agents: Annotated[list[str], add]

    cloud_analysis: str
    ai_analysis: str
    systems_analysis: str

    response: str

    messages: Annotated[list[Any], add_messages]

    action_required: bool
    action_type: str
    action_description: str
    approval_status: str
    action_result: str

    run_id: str | None