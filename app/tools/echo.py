from typing import Any

from app.tools.base import BaseTool
from app.tools.result import ToolResult


class EchoTool(BaseTool):
    @property
    def name(self) -> str:
        return "echo"

    @property
    def description(self) -> str:
        return "Test echo tool."

    async def execute(self, **kwargs: Any) -> ToolResult:
        return ToolResult(success=True, output="echo")
