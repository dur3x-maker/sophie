from typing import Any

from app.tools.base import BaseTool
from app.tools.result import ToolResult


class FilesystemTool(BaseTool):
    @property
    def name(self) -> str:
        return "filesystem"

    @property
    def description(self) -> str:
        return "Filesystem operations tool placeholder."

    async def execute(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError("FilesystemTool is not implemented yet")
