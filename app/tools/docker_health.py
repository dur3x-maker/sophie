from typing import Any

from app.tools.base import BaseTool
from app.tools.executor import ToolExecutor
from app.tools.result import ToolResult
from app.tools.ssh import SSHTool

DOCKER_HEALTH_COMMANDS = (
    "docker compose ps",
    "docker compose logs --tail=50",
)


class DockerHealthTool(BaseTool):
    def __init__(
        self,
        ssh_tool: BaseTool | None = None,
        executor: ToolExecutor | None = None,
    ) -> None:
        self._ssh_tool = ssh_tool or SSHTool()
        self._executor = executor or ToolExecutor()

    @property
    def name(self) -> str:
        return "docker_health"

    @property
    def description(self) -> str:
        return "Checks Docker Compose health on a remote server."

    async def execute(self, **kwargs: Any) -> ToolResult:
        ssh_kwargs = self._ssh_kwargs(kwargs)
        ps_result = await self._executor.execute(
            self._ssh_tool,
            **ssh_kwargs,
            command="docker compose ps",
        )
        logs_result = await self._executor.execute(
            self._ssh_tool,
            **ssh_kwargs,
            command="docker compose logs --tail=50",
        )

        return ToolResult(
            success=ps_result.success and logs_result.success,
            output=self._combine_output(ps_result, logs_result),
            error=ps_result.error or logs_result.error,
            metadata={
                "ps": ps_result.model_dump(mode="json"),
                "logs": logs_result.model_dump(mode="json"),
                "commands": list(DOCKER_HEALTH_COMMANDS),
            },
        )

    def _ssh_kwargs(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        return {
            "host": kwargs["host"],
            "username": kwargs["username"],
            "password": kwargs["password"],
            "timeout": kwargs.get("timeout", 30.0),
        }

    def _combine_output(self, ps_result: ToolResult, logs_result: ToolResult) -> str:
        return (
            f"docker compose ps:\n{ps_result.output}\n\n"
            f"docker compose logs --tail=50:\n{logs_result.output}"
        )
