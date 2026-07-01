from abc import ABC, abstractmethod


class BaseMemory(ABC):
    @abstractmethod
    async def append(self, chat_id: str, role: str, content: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def history(self, chat_id: str) -> list[dict[str, str]]:
        raise NotImplementedError

    @abstractmethod
    async def clear(self, chat_id: str) -> None:
        raise NotImplementedError
