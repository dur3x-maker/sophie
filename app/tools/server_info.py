from typing import Any

from app.tools.base import BaseTool
from app.tools.executor import ToolExecutor
from app.tools.result import ToolResult
from app.tools.ssh import SSHTool

SERVER_INFO_COMMANDS = (
    "uptime",
    "free -h",
    "df -h",
)


class ServerInfoTool(BaseTool):
    def __init__(
        self,
        ssh_tool: BaseTool | None = None,
        executor: ToolExecutor | None = None,
    ) -> None:
        self._ssh_tool = ssh_tool or SSHTool()
        self._executor = executor or ToolExecutor()

    @property
    def name(self) -> str:
        return "server_info"

    @property
    def description(self) -> str:
        return "Collects basic remote server diagnostics."

    async def execute(self, **kwargs: Any) -> ToolResult:
        ssh_kwargs = self._ssh_kwargs(kwargs)
        uptime_result = await self._executor.execute(self._ssh_tool, **ssh_kwargs, command="uptime")
        memory_result = await self._executor.execute(
            self._ssh_tool, **ssh_kwargs, command="free -h"
        )
        disk_result = await self._executor.execute(self._ssh_tool, **ssh_kwargs, command="df -h")

        return ToolResult(
            success=uptime_result.success and memory_result.success and disk_result.success,
            output=self._combine_output(uptime_result, memory_result, disk_result),
            error=uptime_result.error or memory_result.error or disk_result.error,
            metadata={
                "uptime": uptime_result.model_dump(mode="json"),
                "memory": memory_result.model_dump(mode="json"),
                "disk": disk_result.model_dump(mode="json"),
                "commands": list(SERVER_INFO_COMMANDS),
            },
        )

    def _ssh_kwargs(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        return {
            "host": kwargs["host"],
            "username": kwargs["username"],
            "password": kwargs["password"],
            "timeout": kwargs.get("timeout", 30.0),
        }

    def _combine_output(
        self,
        uptime_result: ToolResult,
        memory_result: ToolResult,
        disk_result: ToolResult,
    ) -> str:
        return (
            f"uptime:\n{uptime_result.output}\n\n"
            f"free -h:\n{memory_result.output}\n\n"
            f"df -h:\n{disk_result.output}"
        )
