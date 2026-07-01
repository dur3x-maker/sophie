from abc import ABC, abstractmethod
from typing import Any

from app.tools.result import ToolResult


class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @property
    def requires_confirmation(self) -> bool:
        return False

    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError
