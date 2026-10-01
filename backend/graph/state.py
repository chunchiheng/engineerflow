from typing import TypedDict, Any


class EngineerFlowState(TypedDict):
    user_query: str
    domain: str
    complexity: str
    key_considerations: list[str]
    response: str
    messages: list[Any]