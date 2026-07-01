from typing import Any

from app.tools.base import BaseTool


class FilesystemTool(BaseTool):
    def name(self) -> str:
        return "filesystem"

    def description(self) -> str:
        return "Filesystem operations tool placeholder."

    async def execute(self, **kwargs: Any) -> Any:
        raise NotImplementedError("FilesystemTool is not implemented yet")
