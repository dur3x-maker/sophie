from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class UserCommand(BaseModel):
    id: UUID
    text: str
    source: str
    user_id: str
    created_at: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class WorkerResult(BaseModel):
    success: bool
    message: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)
