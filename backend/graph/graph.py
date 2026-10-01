from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from backend.graph.state import EngineerFlowState
from backend.agents.engineering_agent import engineering_agent
from backend.tools.knowledge_tools import search_engineering_knowledge


# --------------------------------------------------
# Tool Node
# --------------------------------------------------

tool_node = ToolNode(
    [search_engineering_knowledge]
)


# --------------------------------------------------
# Routing Logic
# --------------------------------------------------

def should_continue(state: EngineerFlowState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"


# --------------------------------------------------
# Build Graph
# --------------------------------------------------

builder = StateGraph(EngineerFlowState)


builder.add_node(
    "engineering_agent",
    engineering_agent
)

builder.add_node(
    "tools",
    tool_node
)


# --------------------------------------------------
# Edges
# --------------------------------------------------

builder.add_edge(
    START,
    "engineering_agent"
)


builder.add_conditional_edges(
    "engineering_agent",
    should_continue,
    {
        "tools": "tools",
        "end": END,
    }
)


builder.add_edge(
    "tools",
    "engineering_agent"
)


graph = builder.compile()