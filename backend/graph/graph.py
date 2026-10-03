# from langgraph.graph import StateGraph, START, END
# from langgraph.prebuilt import ToolNode

# from backend.graph.state import EngineerFlowState
# from backend.agents.engineering_agent import engineering_agent
# from backend.tools.knowledge_tools import search_engineering_knowledge


# # --------------------------------------------------
# # Tool Node
# # --------------------------------------------------

# tool_node = ToolNode(
#     [search_engineering_knowledge]
# )


# # --------------------------------------------------
# # Routing Logic
# # --------------------------------------------------

# def should_continue(state: EngineerFlowState):

#     last_message = state["messages"][-1]

#     if last_message.tool_calls:
#         return "tools"

#     return "end"


# # --------------------------------------------------
# # Build Graph
# # --------------------------------------------------

# builder = StateGraph(EngineerFlowState)


# builder.add_node(
#     "engineering_agent",
#     engineering_agent
# )

# builder.add_node(
#     "tools",
#     tool_node
# )


# # --------------------------------------------------
# # Edges
# # --------------------------------------------------

# builder.add_edge(
#     START,
#     "engineering_agent"
# )


# builder.add_conditional_edges(
#     "engineering_agent",
#     should_continue,
#     {
#         "tools": "tools",
#         "end": END,
#     }
# )


# builder.add_edge(
#     "tools",
#     "engineering_agent"
# )


# graph = builder.compile()


from langgraph.graph import StateGraph, START, END

from backend.graph.state import EngineerFlowState

from backend.agents.supervisor import supervisor_agent
from backend.agents.cloud_agent import cloud_agent
from backend.agents.ai_agent import ai_agent
from backend.agents.systems_agent import systems_agent
from backend.agents.aggregator import aggregator_agent


builder = StateGraph(EngineerFlowState)


builder.add_node("supervisor", supervisor_agent)
builder.add_node("cloud_agent", cloud_agent)
builder.add_node("ai_agent", ai_agent)
builder.add_node("systems_agent", systems_agent)
builder.add_node("aggregator", aggregator_agent)


builder.add_edge(START, "supervisor")


def route_after_supervisor(state: EngineerFlowState):

    selected_agents = state["selected_agents"]
    completed_agents = state["completed_agents"]

    for agent in selected_agents:

        if agent not in completed_agents:

            return f"{agent}_agent"

    return "aggregator"


builder.add_conditional_edges(
    "supervisor",
    route_after_supervisor,
    {
        "cloud_agent": "cloud_agent",
        "ai_agent": "ai_agent",
        "systems_agent": "systems_agent",
        "aggregator": "aggregator",
    }
)


builder.add_conditional_edges(
    "cloud_agent",
    route_after_supervisor,
    {
        "cloud_agent": "cloud_agent",
        "ai_agent": "ai_agent",
        "systems_agent": "systems_agent",
        "aggregator": "aggregator",
    },
)

builder.add_conditional_edges(
    "ai_agent",
    route_after_supervisor,
    {
        "cloud_agent": "cloud_agent",
        "ai_agent": "ai_agent",
        "systems_agent": "systems_agent",
        "aggregator": "aggregator",
    },
)

builder.add_conditional_edges(
    "systems_agent",
    route_after_supervisor,
    {
        "cloud_agent": "cloud_agent",
        "ai_agent": "ai_agent",
        "systems_agent": "systems_agent",
        "aggregator": "aggregator",
    },
)

builder.add_edge("aggregator", END)

graph = builder.compile()