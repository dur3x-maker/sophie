import asyncio

import pytest

from app.core.exceptions import LLMProviderError
from app.providers.openrouter import OpenRouterProvider


def test_openrouter_provider_does_not_request_without_api_key() -> None:
    provider = OpenRouterProvider(
        api_key="",
        model="openrouter/model",
        base_url="https://openrouter.ai/api/v1",
    )

    with pytest.raises(LLMProviderError, match="API key and model"):
        asyncio.run(provider.chat([{"role": "user", "content": "hello"}]))


def test_openrouter_provider_does_not_request_without_model() -> None:
    provider = OpenRouterProvider(
        api_key="token",
        model="",
        base_url="https://openrouter.ai/api/v1",
    )

    with pytest.raises(LLMProviderError, match="API key and model"):
        asyncio.run(provider.chat([{"role": "user", "content": "hello"}]))
