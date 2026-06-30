from abc import ABC, abstractmethod


class BaseMemory(ABC):
    @abstractmethod
    async def add_message(self, user_id: str, role: str, content: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_history(self, user_id: str) -> list[dict[str, str]]:
        raise NotImplementedError

    @abstractmethod
    async def clear(self, user_id: str) -> None:
        raise NotImplementedError
