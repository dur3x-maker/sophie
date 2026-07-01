from time import perf_counter
from typing import Any

from app.security.policy import SecurityPolicy
from app.security.validator import SecurityValidator
from app.tools.base import BaseTool
from app.tools.result import ToolResult


class ToolExecutor:
    def __init__(
        self,
        security_validator: SecurityValidator | None = None,
        security_policy: SecurityPolicy | None = None,
    ) -> None:
        self._security_policy = security_policy or SecurityPolicy()
        self._security_validator = security_validator or SecurityValidator()

    async def execute(self, tool: BaseTool, **kwargs: Any) -> ToolResult:
        started_at = perf_counter()

        try:
            self._validate_command_arguments(kwargs)

            result = await tool.execute(**kwargs)
        except Exception as exc:
            return ToolResult(
                success=False,
                output="",
                error=str(exc),
                execution_time=perf_counter() - started_at,
                metadata={
                    "tool_name": tool.name,
                    "exception_type": type(exc).__name__,
                },
            )

        return result.model_copy(
            update={
                "execution_time": result.execution_time or perf_counter() - started_at,
                "metadata": {"tool_name": tool.name, **result.metadata},
            }
        )

    def _validate_command_arguments(self, kwargs: dict[str, Any]) -> None:
        for argument_name in self._security_policy.command_argument_names:
            command = kwargs.get(argument_name)
            if isinstance(command, str):
                self._security_validator.validate(command)
