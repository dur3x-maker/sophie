from typing import Any

from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    success: bool
    output: str = ""
    stdout: str = ""
    stderr: str = ""
    exit_code: int | None = None
    error: str | None = None
    execution_time: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)
