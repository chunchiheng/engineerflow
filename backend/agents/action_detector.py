from typing import Literal

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from backend.graph.state import EngineerFlowState


class ActionDetection(BaseModel):
    action_required: bool = Field(
        description="Whether the user's request requires human approval before execution."
    )

    action_type: Literal[
        "none",
        "deploy",
        "create",
        "delete",
        "modify",
    ] = Field(
        description="The type of action that requires approval."
    )

    action_description: str = Field(
        description="A concise description of the action that would require human approval."
    )


llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0,
)

action_detector = llm.with_structured_output(ActionDetection)


SYSTEM_PROMPT = """
You are the Action Detection component of EngineerFlow.

Your responsibility is to determine whether the user's request
requires human approval before an external or potentially
impactful engineering action can be executed.

Actions that require human approval include:

- deploying applications or infrastructure
- creating cloud resources
- deleting resources
- modifying production infrastructure
- modifying security-sensitive configurations

Pure information, analysis, research, comparison, recommendation,
or architecture discussion does NOT require approval.

Examples:

"Should I use EC2 or Lambda?"
-> action_required = false
-> action_type = "none"

"Should I migrate my RAG application from EC2 to Lambda?"
-> action_required = false
-> action_type = "none"

"Deploy the application to AWS Lambda."
-> action_required = true
-> action_type = "deploy"

"Create an S3 bucket for the application."
-> action_required = true
-> action_type = "create"

"Delete the production EC2 instance."
-> action_required = true
-> action_type = "delete"

"Change the production security group to allow inbound traffic."
-> action_required = true
-> action_type = "modify"

Important rules:

1. Do not require approval for analysis or recommendations.
2. Require approval when EngineerFlow would actually perform
   an external or potentially impactful engineering action.
3. Do not assume that discussing an action means the action
   should be executed.
4. If no action is required, use action_type = "none".
5. Keep action_description concise.
"""


def detect_action(state: EngineerFlowState):
    user_query = state["user_query"]

    messages = [
        ("system", SYSTEM_PROMPT),
        ("human", user_query),
    ]

    result = action_detector.invoke(messages)

    return {
        "action_required": result.action_required,
        "action_type": result.action_type,
        "action_description": result.action_description,
        "approval_status": (
            "pending"
            if result.action_required
            else "not_required"
        ),
    }