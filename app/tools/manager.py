from typing import Any

from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.tools.result import ToolResult


class ToolManager:
    def __init__(
        self,
        registry: ToolRegistry | None = None,
        executor: ToolExecutor | None = None,
    ) -> None:
        self._registry = registry or ToolRegistry()
        self._executor = executor or ToolExecutor()

    async def execute(self, tool_name: str, **kwargs: Any) -> ToolResult:
        try:
            tool = self._registry.get(tool_name)
        except KeyError:
            return ToolResult(
                success=False,
                output="",
                error=f"Unknown tool: {tool_name}",
                metadata={"tool_name": tool_name},
            )

        return await self._executor.execute(tool, **kwargs)
