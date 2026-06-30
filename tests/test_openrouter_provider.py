import asyncio
from typing import Any

import httpx
import pytest

from app.core.exceptions import LLMProviderError
from app.domain.commands import UserCommand
from app.llm.manager import LLMManager
from app.providers.openrouter import OpenRouterProvider
from app.workers.echo import LLM_FALLBACK_MESSAGE, EchoWorker


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


@pytest.mark.parametrize("status_code", [400, 401, 404])
def test_openrouter_http_error_logs_response_and_echo_worker_returns_fallback(
    monkeypatch: pytest.MonkeyPatch,
    status_code: int,
) -> None:
    logs: list[str] = []
    response_body = f'{{"error":"status-{status_code}"}}'

    class FakeLogger:
        def error(self, message: str, **kwargs: object) -> None:
            logs.append(message.format(**kwargs))

    class FakeAsyncClient:
        def __init__(self, **kwargs: object) -> None:
            pass

        async def __aenter__(self) -> "FakeAsyncClient":
            return self

        async def __aexit__(self, *args: object) -> None:
            return None

        async def post(
            self,
            url: str,
            headers: dict[str, str],
            json: dict[str, Any],
        ) -> httpx.Response:
            request = httpx.Request(
                "POST",
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=json,
            )
            return httpx.Response(status_code=status_code, text=response_body, request=request)

    monkeypatch.setattr("app.providers.openrouter.logger", FakeLogger())
    monkeypatch.setattr("app.providers.openrouter.httpx.AsyncClient", FakeAsyncClient)

    provider = OpenRouterProvider(
        api_key="token",
        model="openai/gpt-oss-120b:free",
        base_url="https://openrouter.ai/api/v1",
    )
    worker = EchoWorker(llm_manager=LLMManager(provider=provider))

    result = asyncio.run(worker.handle(_command("hello")))

    assert result.success is False
    assert result.message == LLM_FALLBACK_MESSAGE
    assert len(logs) == 1
    assert "https://openrouter.ai/api/v1/chat/completions" in logs[0]
    assert "openai/gpt-oss-120b:free" in logs[0]
    assert f"Status:\n{status_code}" in logs[0]
    assert response_body in logs[0]
    assert "HTTPStatusError" in logs[0]


def _command(text: str) -> UserCommand:
    from datetime import UTC, datetime
    from uuid import uuid4

    return UserCommand(
        id=uuid4(),
        text=text,
        source="test",
        user_id="user-1",
        created_at=datetime.now(UTC),
    )
