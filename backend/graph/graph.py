from langgraph.graph import StateGraph, START, END

from backend.graph.state import EngineerFlowState

from backend.agents.supervisor import supervisor_agent
from backend.agents.cloud_agent import cloud_agent
from backend.agents.ai_agent import ai_agent
from backend.agents.systems_agent import systems_agent
from backend.agents.aggregator import aggregator_agent
from backend.agents.action_detector import detect_action
from backend.agents.approval_node import approval_node
from backend.agents.action_executor import action_executor
from backend.agents.persistence_node import persist_engineering_run_node



builder = StateGraph(EngineerFlowState)


builder.add_node("supervisor", supervisor_agent)
builder.add_node("cloud_agent", cloud_agent)
builder.add_node("ai_agent", ai_agent)
builder.add_node("systems_agent", systems_agent)
builder.add_node("aggregator", aggregator_agent)
builder.add_node("action_detector", detect_action)
builder.add_node("approval_node", approval_node)
builder.add_node("action_executor", action_executor)
builder.add_node(
    "persist_engineering_run",
    persist_engineering_run_node,
)



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

builder.add_edge("aggregator", "action_detector")

builder.add_edge("action_detector", "persist_engineering_run")

builder.add_edge("persist_engineering_run", "approval_node")


def route_after_approval(state: EngineerFlowState):
    if state["approval_status"] == "approved":
        return "action_executor"

    if state["approval_status"] == "rejected":
        return END

    if state["approval_status"] == "not_required":
        return END

    raise ValueError(
        f"Unexpected approval status: "
        f"{state['approval_status']}"
    )


builder.add_conditional_edges(
    "approval_node",
    route_after_approval,
)

builder.add_edge("action_executor", END)


def build_graph(checkpointer):
    """
    Compile EngineerFlow using the provided checkpointer.

    The caller manages the checkpointer's connection lifetime.
    """
    return builder.compile(
        checkpointer=checkpointer
    )