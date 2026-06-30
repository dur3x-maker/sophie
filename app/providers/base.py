from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    async def chat(self, messages: list[dict[str, str]]) -> str:
        raise NotImplementedError
