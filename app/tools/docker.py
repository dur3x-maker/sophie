from typing import Any

from app.tools.base import BaseTool
from app.tools.result import ToolResult


class DockerTool(BaseTool):
    @property
    def name(self) -> str:
        return "docker"

    @property
    def description(self) -> str:
        return "Docker operations tool placeholder."

    async def execute(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError("DockerTool is not implemented yet")
