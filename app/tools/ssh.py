from typing import Any

from app.tools.base import BaseTool
from app.tools.result import ToolResult


class SSHTool(BaseTool):
    @property
    def name(self) -> str:
        return "ssh"

    @property
    def description(self) -> str:
        return "SSH operations tool placeholder."

    async def execute(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError("SSHTool is not implemented yet")
