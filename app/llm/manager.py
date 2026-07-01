from app.providers.base import BaseProvider


class LLMManager:
    def __init__(self, provider: BaseProvider) -> None:
        self._provider = provider

    async def chat(self, messages: list[dict[str, str]]) -> str:
        return await self._provider.chat(messages)
