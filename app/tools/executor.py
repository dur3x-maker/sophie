from time import perf_counter
from typing import Any

from app.tools.base import BaseTool
from app.tools.result import ToolResult


class ToolExecutor:
    async def execute(self, tool: BaseTool, **kwargs: Any) -> ToolResult:
        started_at = perf_counter()

        try:
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
