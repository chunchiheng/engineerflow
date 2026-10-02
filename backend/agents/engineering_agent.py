# from typing import TypedDict

# from langchain_openai import ChatOpenAI

# from backend.graph.state import EngineerFlowState


# class EngineeringAnalysis(TypedDict):
#     domain: str
#     complexity: str
#     key_considerations: list[str]
#     answer: str


# llm = ChatOpenAI(
#     model="gpt-5-mini",
#     temperature=0
# )


# SYSTEM_PROMPT = """
# You are EngineerFlow, an AI engineering copilot.

# Your role is to help engineers analyze technical
# architecture and engineering decisions.

# Your main areas are:

# - Cloud Engineering
# - AI Engineering
# - Systems Engineering

# For each question:

# 1. Understand the engineering problem.
# 2. Identify the important technical considerations.
# 3. Explain relevant trade-offs.
# 4. Avoid inventing facts.
# 5. Clearly distinguish assumptions from known information.
# 6. Provide a practical engineering-oriented answer.

# Classify the question into one of these domains:

# - cloud
# - ai
# - systems

# Classify complexity as:

# - simple
# - medium
# - complex

# Return a structured engineering analysis.
# """


# structured_llm = llm.with_structured_output(EngineeringAnalysis)



# def engineering_agent(state: EngineerFlowState) -> EngineerFlowState:

#     messages = [
#         ("system", SYSTEM_PROMPT),
#         ("human", state["user_query"]),
#     ]

#     result = structured_llm.invoke(messages)

#     return {
#         **state,
#         "domain": result["domain"],
#         "complexity": result["complexity"],
#         "key_considerations": result["key_considerations"],
#         "response": result["answer"],
#     }


from langchain_openai import ChatOpenAI

from backend.graph.state import EngineerFlowState
from backend.tools.knowledge_tools import search_engineering_knowledge


llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0,
)

llm_with_tools = llm.bind_tools(
    [search_engineering_knowledge]
)


SYSTEM_PROMPT = """
You are EngineerFlow, an AI engineering copilot.

Your role is to help engineers analyze technical
architecture and engineering decisions.

Your main areas are:

- Cloud Engineering
- AI Engineering
- Systems Engineering

You have access to an engineering knowledge base.

IMPORTANT:

For questions about engineering concepts that may
be covered by the knowledge base, you MUST use the
search_engineering_knowledge tool before answering.

After receiving the tool result, use the retrieved
information to provide the final answer.

Do not answer from your own knowledge when the
knowledge base can provide relevant information.

Avoid inventing facts.

Clearly distinguish assumptions from known information.
"""


def engineering_agent(state: EngineerFlowState):
    messages = state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        **state,
        "messages": [response],
    }