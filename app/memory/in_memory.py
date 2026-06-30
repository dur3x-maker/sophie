from app.memory.base import BaseMemory


class InMemoryMemory(BaseMemory):
    def __init__(self, max_messages: int = 20) -> None:
        self._storage: dict[str, list[dict[str, str]]] = {}
        self._max_messages = max_messages

    async def add_message(self, user_id: str, role: str, content: str) -> None:
        messages = self._storage.setdefault(user_id, [])
        messages.append({"role": role, "content": content})
        self._storage[user_id] = messages[-self._max_messages :]

    async def get_history(self, user_id: str) -> list[dict[str, str]]:
        return list(self._storage.get(user_id, []))

    async def clear(self, user_id: str) -> None:
        self._storage.pop(user_id, None)
