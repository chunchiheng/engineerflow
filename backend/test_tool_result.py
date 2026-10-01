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

After receiving the tool result, use the
information from the tool to provide the final answer.
"""
    ),
    (
        "human",
        "What is AWS Lambda?"
    ),
]


# --------------------------------------------------
# Step 1: Ask the LLM
# --------------------------------------------------

response = llm_with_tools.invoke(messages)

print("\n=== LLM Tool Call ===")
print(response.tool_calls)


# --------------------------------------------------
# Step 2: Add the LLM response to the conversation
# --------------------------------------------------

messages.append(response)


# --------------------------------------------------
# Step 3: Execute the tool
# --------------------------------------------------

for tool_call in response.tool_calls:

    if tool_call["name"] == "search_engineering_knowledge":

        tool_result = search_engineering_knowledge.invoke(
            tool_call["args"]
        )

        print("\n=== Tool Result ===")
        print(tool_result)

        # Add the tool result back to the conversation
        messages.append(
            {
                "role": "tool",
                "content": tool_result,
                "tool_call_id": tool_call["id"],
            }
        )


# --------------------------------------------------
# Step 4: Ask the LLM again using the tool result
# --------------------------------------------------

final_response = llm_with_tools.invoke(messages)


print("\n=== Final Answer ===")
print(final_response.content)