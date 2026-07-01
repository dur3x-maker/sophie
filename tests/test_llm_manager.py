import asyncio

import pytest

from app.core.exceptions import LLMProviderError
from app.llm.manager import LLMManager
from app.providers.base import BaseProvider


class FakeProvider(BaseProvider):
    async def chat(self, messages: list[dict[str, str]]) -> str:
        assert messages == [{"role": "user", "content": "hello"}]
        return "hi"


class FailingProvider(BaseProvider):
    async def chat(self, messages: list[dict[str, str]]) -> str:
        raise LLMProviderError("provider failed")


def test_llm_manager_can_be_created() -> None:
    manager = LLMManager(provider=FakeProvider())

    assert isinstance(manager, LLMManager)


def test_llm_manager_chat_returns_provider_text() -> None:
    manager = LLMManager(provider=FakeProvider())

    result = asyncio.run(manager.chat([{"role": "user", "content": "hello"}]))

    assert result == "hi"


def test_llm_manager_propagates_provider_error() -> None:
    manager = LLMManager(provider=FailingProvider())

    with pytest.raises(LLMProviderError, match="provider failed"):
        asyncio.run(manager.chat([{"role": "user", "content": "hello"}]))
