from langgraph.graph import StateGraph, START, END

from backend.graph.state import EngineerFlowState
from backend.agents.engineering_agent import engineering_agent


builder = StateGraph(EngineerFlowState)

builder.add_node(
    "engineering_agent",
    engineering_agent
)

builder.add_edge(
    START,
    "engineering_agent"
)

builder.add_edge(
    "engineering_agent",
    END
)

graph = builder.compile()