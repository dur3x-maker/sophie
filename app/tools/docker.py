from typing import Any

from app.tools.base import BaseTool


class DockerTool(BaseTool):
    def name(self) -> str:
        return "docker"

    def description(self) -> str:
        return "Docker operations tool placeholder."

    async def execute(self, **kwargs: Any) -> Any:
        raise NotImplementedError("DockerTool is not implemented yet")
