from langchain_openai import ChatOpenAI
from backend.graph.state import EngineerFlowState
from backend.tools.knowledge_tools import search_engineering_knowledge
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
    [search_engineering_knowledge]
)


SYSTEM_PROMPT = """
You are the AI Engineering Agent in EngineerFlow.

Your responsibility is to analyze engineering problems
related to artificial intelligence and machine learning systems.

Focus on topics such as:

- LLM applications
- RAG
- agentic AI
- vector databases
- embeddings
- model selection
- fine-tuning
- inference
- evaluation
- AI architecture
- AI security

Use the search_engineering_knowledge tool when relevant
engineering knowledge is needed.

Provide practical and technically grounded analysis.

Do not make up facts.
Clearly distinguish assumptions from known information.
"""


def ai_agent(state: EngineerFlowState):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=state["user_query"]),
    ]

    response = llm_with_tools.invoke(messages)

    if response.tool_calls:

        tool_call = response.tool_calls[0]

        tool_result = search_engineering_knowledge.invoke(
            tool_call["args"]
        )

        messages.append(response)

        

        messages.append(
            ToolMessage(
                content=tool_result,
                tool_call_id=tool_call["id"],
            )
        )

        final_response = llm_with_tools.invoke(messages)

        return {
            "ai_analysis": final_response.content,
            "completed_agents": ["ai"],
        }

    return {
        "ai_analysis": response.content,
        "completed_agents": ["ai"],
    }