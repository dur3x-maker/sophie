from typing import Any

from app.tools.base import BaseTool


class ShellTool(BaseTool):
    def name(self) -> str:
        return "shell"

    def description(self) -> str:
        return "Shell command tool placeholder."

    async def execute(self, **kwargs: Any) -> Any:
        raise NotImplementedError("ShellTool is not implemented yet")
