from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        raise NotImplementedError
