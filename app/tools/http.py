from typing import Any

from app.tools.base import BaseTool
from app.tools.result import ToolResult


class HttpTool(BaseTool):
    @property
    def name(self) -> str:
        return "http"

    @property
    def description(self) -> str:
        return "HTTP request tool placeholder."

    async def execute(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError("HttpTool is not implemented yet")
