from langchain_openai import ChatOpenAI

from backend.graph.state import EngineerFlowState


llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0,
)


SYSTEM_PROMPT = """
You are the Final Engineering Decision Agent in EngineerFlow.

Your responsibility is to combine the analysis produced by
specialized engineering agents into one clear and practical
engineering answer.

You may receive analysis from:

- Cloud Engineering Agent
- AI Engineering Agent
- Systems Engineering Agent

Use the provided specialized analyses as the primary evidence.

Your final answer should:

1. Clearly answer the user's question.
2. Summarize the relevant findings from each agent.
3. Explain important trade-offs.
4. Identify assumptions or missing information.
5. Avoid inventing facts.
6. Provide a practical engineering recommendation when
   the available evidence supports one.

Do not mention internal agent orchestration unless it is
useful for explaining the answer.
"""


def aggregator_agent(state: EngineerFlowState):

    analyses = []

    if state["cloud_analysis"]:
        analyses.append(
            f"=== Cloud Engineering Analysis ===\n"
            f"{state['cloud_analysis']}"
        )

    if state["ai_analysis"]:
        analyses.append(
            f"=== AI Engineering Analysis ===\n"
            f"{state['ai_analysis']}"
        )

    if state["systems_analysis"]:
        analyses.append(
            f"=== Systems Engineering Analysis ===\n"
            f"{state['systems_analysis']}"
        )

    combined_analysis = "\n\n".join(analyses)

    response = llm.invoke([
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
User question:

{state["user_query"]}

Specialized engineering analyses:

{combined_analysis}
""",
        },
    ])

    return {
        "response": response.content,
    }