from typing import Any

from app.tools.base import BaseTool


class SSHTool(BaseTool):
    def name(self) -> str:
        return "ssh"

    def description(self) -> str:
        return "SSH operations tool placeholder."

    async def execute(self, **kwargs: Any) -> Any:
        raise NotImplementedError("SSHTool is not implemented yet")
