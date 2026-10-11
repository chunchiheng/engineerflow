
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class TaskCreateRequest(BaseModel):
    user_query: str = Field(
        min_length=1,
        max_length=5000,
    )

    @field_validator("user_query")
    @classmethod
    def validate_user_query(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "user_query cannot be empty."
            )

        return value


class TaskCreateResponse(BaseModel):
    run_id: UUID
    status: str



from datetime import datetime
from typing import Literal


TaskStatus = Literal[
    "queued",
    "running",
    "awaiting_approval",
    "completed",
    "failed",
]


class TaskStatusResponse(BaseModel):
    run_id: UUID
    status: TaskStatus
    user_query: str

    celery_task_id: str | None = None
    final_response: str | None = None
    approval_status: str | None = None
    action_result: str | None = None
    error_message: str | None = None

    created_at: datetime


class TaskApprovalRequest(BaseModel):
    decision: Literal["approved", "rejected"]


class TaskApprovalResponse(BaseModel):
    run_id: UUID
    status: Literal["running"]
    decision: Literal["approved", "rejected"]