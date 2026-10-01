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


# Step 1: Ask the LLM
response = llm_with_tools.invoke(messages)

print("\nLLM Response:")
print(response)

print("\nTool calls:")
print(response.tool_calls)


# Step 2: Execute the tool
for tool_call in response.tool_calls:

    if tool_call["name"] == "search_engineering_knowledge":

        tool_result = search_engineering_knowledge.invoke(
            tool_call["args"]
        )

        print("\nTool Result:")
        print(tool_result)