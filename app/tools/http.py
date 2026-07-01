from typing import Any

from app.tools.base import BaseTool


class HttpTool(BaseTool):
    def name(self) -> str:
        return "http"

    def description(self) -> str:
        return "HTTP request tool placeholder."

    async def execute(self, **kwargs: Any) -> Any:
        raise NotImplementedError("HttpTool is not implemented yet")
