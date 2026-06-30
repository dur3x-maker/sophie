import asyncio
from datetime import UTC, datetime
from uuid import uuid4

from app.core.exceptions import LLMProviderError
from app.domain.commands import UserCommand
from app.llm.manager import LLMManager
from app.workers.echo import EchoWorker


class FakeLLMManager(LLMManager):
    def __init__(self, response: str | None = None, error: LLMProviderError | None = None) -> None:
        self._response = response
        self._error = error

    async def chat(self, text: str) -> str:
        if self._error is not None:
            raise self._error
        return self._response or f"model: {text}"


def test_echo_worker_returns_llm_response() -> None:
    worker = EchoWorker(llm_manager=FakeLLMManager(response="hi from llm"))

    result = asyncio.run(worker.handle(_command("hello")))

    assert result.success is True
    assert result.message == "hi from llm"


def test_echo_worker_returns_error_result_on_provider_error() -> None:
    worker = EchoWorker(llm_manager=FakeLLMManager(error=LLMProviderError("provider failed")))

    result = asyncio.run(worker.handle(_command("hello")))

    assert result.success is False
    assert result.message == "provider failed"


def _command(text: str) -> UserCommand:
    return UserCommand(
        id=uuid4(),
        text=text,
        source="test",
        user_id="user-1",
        created_at=datetime.now(UTC),
    )
