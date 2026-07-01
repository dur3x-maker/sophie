from typing import Any

from app.tools.base import BaseTool
from app.tools.result import ToolResult


class ShellTool(BaseTool):
    @property
    def name(self) -> str:
        return "shell"

    @property
    def description(self) -> str:
        return "Shell command tool placeholder."

    async def execute(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError("ShellTool is not implemented yet")
