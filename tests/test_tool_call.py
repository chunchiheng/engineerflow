from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

from backend.tools.knowledge_tools import search_engineering_knowledge


llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0
)

llm_with_tools = llm.bind_tools(
    [search_engineering_knowledge]
)


messages = [
    (
        "system",
        """
You are an engineering assistant.

You have access to a tool called
search_engineering_knowledge.

For this test, you MUST use the
search_engineering_knowledge tool to answer
the user's question.

Do not answer from your own knowledge.
"""
    ),
    (
        "human",
        "What is AWS Lambda?"
    ),
]


response = llm_with_tools.invoke(messages)

print("\nResponse:")
print(response)

print("\nContent:")
print(response.content)

print("\nTool calls:")
print(response.tool_calls)