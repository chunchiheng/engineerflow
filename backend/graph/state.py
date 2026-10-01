from typing import TypedDict


class EngineerFlowState(TypedDict):
    user_query: str
    domain: str
    complexity: str
    key_considerations: list[str]
    response: str