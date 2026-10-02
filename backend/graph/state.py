from typing import TypedDict, Any, Annotated
from langgraph.graph.message import add_messages


class EngineerFlowState(TypedDict):
    user_query: str
    domain: str
    complexity: str
    key_considerations: list[str]
    response: str
    messages: Annotated[list[Any], add_messages]