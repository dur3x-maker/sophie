from collections.abc import Iterable

from app.tools.base import BaseTool
from app.tools.docker import DockerTool
from app.tools.docker_health import DockerHealthTool
from app.tools.filesystem import FilesystemTool
from app.tools.git import GitTool
from app.tools.http import HttpTool
from app.tools.server_info import ServerInfoTool
from app.tools.shell import ShellTool
from app.tools.ssh import SSHTool


class ToolRegistry:
    def __init__(self, tools: Iterable[type[BaseTool] | BaseTool] | None = None) -> None:
        registered_tools = tools or (
            SSHTool,
            DockerHealthTool,
            ServerInfoTool,
            ShellTool,
            DockerTool,
            GitTool,
            FilesystemTool,
            HttpTool,
        )
        self._tool_classes = {
            self._tool_name(tool): tool if isinstance(tool, type) else type(tool)
            for tool in registered_tools
        }

    def get(self, tool_name: str) -> BaseTool:
        return self._tool_classes[tool_name]()

    def get_many(self, tool_names: Iterable[str]) -> list[BaseTool]:
        return [self.get(tool_name) for tool_name in tool_names]

    def names(self) -> list[str]:
        return list(self._tool_classes)

    def _tool_name(self, tool: type[BaseTool] | BaseTool) -> str:
        return tool().name if isinstance(tool, type) else tool.name
