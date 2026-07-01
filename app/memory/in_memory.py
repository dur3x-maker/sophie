from app.memory.base import BaseMemory


class InMemoryConversationMemory(BaseMemory):
    def __init__(self, max_messages: int = 20) -> None:
        self._storage: dict[str, list[dict[str, str]]] = {}
        self._max_messages = max_messages

    async def append(self, chat_id: str, role: str, content: str) -> None:
        messages = self._storage.setdefault(chat_id, [])
        messages.append({"role": role, "content": content})
        self._storage[chat_id] = messages[-self._max_messages :]

    async def history(self, chat_id: str) -> list[dict[str, str]]:
        return list(self._storage.get(chat_id, []))

    async def clear(self, chat_id: str) -> None:
        self._storage.pop(chat_id, None)

    async def add_message(self, user_id: str, role: str, content: str) -> None:
        await self.append(user_id, role, content)

    async def get_history(self, user_id: str) -> list[dict[str, str]]:
        return await self.history(user_id)


InMemoryMemory = InMemoryConversationMemory
