from langchain_openai import ChatOpenAI
from backend.graph.state import EngineerFlowState
from backend.tools.knowledge_tools import search_engineering_knowledge
from backend.memory.memory_tools import (
    search_previous_engineering_decisions,
)
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
)

llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0
)

llm_with_tools = llm.bind_tools(
    [
        search_engineering_knowledge,
        search_previous_engineering_decisions,
    ]
)


SYSTEM_PROMPT = """
You are the Cloud Engineering Agent in EngineerFlow.

Your responsibility is to analyze engineering problems
related to cloud computing and cloud architecture.

Focus on topics such as:

- AWS services
- cloud architecture
- compute
- storage
- networking
- scalability
- reliability
- cloud cost
- security
- deployment models

Use the search_engineering_knowledge tool when relevant
engineering knowledge is needed.

After receiving tool results, use the retrieved information
to provide the final analysis.

You also have access to a memory tool called
search_previous_engineering_decisions.

Use the memory tool when previous engineering decisions
may provide useful context for the current question.

Do not use the memory tool for every question.

Use your engineering judgment to decide whether
previous decisions are relevant.

Do not treat previous decisions as authoritative.
They are historical context and may not apply to
the current problem.

Do not make up facts.
Clearly distinguish assumptions from known information.
"""


def cloud_agent(state: EngineerFlowState):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=state["user_query"]),
    ]

    response = llm_with_tools.invoke(messages)

    if response.tool_calls:

        tool_messages = []

        for tool_call in response.tool_calls:

            if tool_call["name"] == "search_engineering_knowledge":
                tool_result = search_engineering_knowledge.invoke(
                    tool_call["args"]
                )

            elif tool_call["name"] == "search_previous_engineering_decisions":
                tool_result = search_previous_engineering_decisions.invoke(
                    tool_call["args"]
                )

            else:
                tool_result = "Unknown tool."

            tool_messages.append(
                ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call["id"],
                )
            )

        messages.append(response)
        messages.extend(tool_messages)

        final_response = llm_with_tools.invoke(messages)

        return {
            "cloud_analysis": final_response.content,
            "completed_agents": ["cloud"],
        }

    return {
        "cloud_analysis": response.content,
        "completed_agents": ["cloud"],
    }