from typing import Any

from app.tools.registry import ToolRegistry


class ToolManager:
    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self._registry = registry or ToolRegistry()

    async def execute(self, tool_name: str, **kwargs: Any) -> Any:
        tool = self._registry.get(tool_name)
        return await tool.execute(**kwargs)
