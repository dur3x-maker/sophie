from typing import Any

from app.tools.base import BaseTool


class GitTool(BaseTool):
    def name(self) -> str:
        return "git"

    def description(self) -> str:
        return "Git operations tool placeholder."

    async def execute(self, **kwargs: Any) -> Any:
        raise NotImplementedError("GitTool is not implemented yet")
