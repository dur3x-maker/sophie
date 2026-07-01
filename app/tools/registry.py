from collections.abc import Iterable

from app.tools.base import BaseTool
from app.tools.docker import DockerTool
from app.tools.filesystem import FilesystemTool
from app.tools.git import GitTool
from app.tools.http import HttpTool
from app.tools.shell import ShellTool
from app.tools.ssh import SSHTool


class ToolRegistry:
    def __init__(self, tools: Iterable[BaseTool] | None = None) -> None:
        registered_tools = tools or (
            SSHTool(),
            ShellTool(),
            DockerTool(),
            GitTool(),
            FilesystemTool(),
            HttpTool(),
        )
        self._tools = {tool.name(): tool for tool in registered_tools}

    def get(self, tool_name: str) -> BaseTool:
        return self._tools[tool_name]

    def get_many(self, tool_names: Iterable[str]) -> list[BaseTool]:
        return [self.get(tool_name) for tool_name in tool_names]

    def names(self) -> list[str]:
        return list(self._tools)
