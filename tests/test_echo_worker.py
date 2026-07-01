import asyncio
from datetime import UTC, datetime
from uuid import uuid4

from app.core.exceptions import LLMProviderError
from app.domain.commands import UserCommand
from app.llm.manager import LLMManager
from app.llm.prompt_builder import PromptBuilder
from app.memory.in_memory import InMemoryConversationMemory
from app.workers.echo import LLM_FALLBACK_MESSAGE, EchoWorker


class FakeLLMManager(LLMManager):
    def __init__(self, response: str | None = None, error: LLMProviderError | None = None) -> None:
        self._response = response
        self._error = error
        self.messages: list[list[dict[str, str]]] = []

    async def chat(self, messages: list[dict[str, str]]) -> str:
        self.messages.append(messages)
        if self._error is not None:
            raise self._error
        return self._response or f"model: {messages[-1]['content']}"


def test_echo_worker_returns_llm_response() -> None:
    worker = EchoWorker(
        llm_manager=FakeLLMManager(response="hi from llm"),
        memory=InMemoryConversationMemory(),
        prompt_builder=PromptBuilder(),
    )

    result = asyncio.run(worker.handle(_command("hello")))

    assert result.success is True
    assert result.message == "hi from llm"


def test_echo_worker_returns_error_result_on_provider_error() -> None:
    worker = EchoWorker(
        llm_manager=FakeLLMManager(error=LLMProviderError("provider failed")),
        memory=InMemoryConversationMemory(),
        prompt_builder=PromptBuilder(),
    )

    result = asyncio.run(worker.handle(_command("hello")))

    assert result.success is False
    assert result.message == LLM_FALLBACK_MESSAGE


def test_echo_worker_passes_previous_turn_to_llm() -> None:
    llm_manager = FakeLLMManager()
    worker = EchoWorker(
        llm_manager=llm_manager,
        memory=InMemoryConversationMemory(),
        prompt_builder=PromptBuilder(),
    )

    asyncio.run(worker.handle(_command("first")))
    asyncio.run(worker.handle(_command("second")))

    second_call = llm_manager.messages[1]

    assert {"role": "user", "content": "first"} in second_call
    assert {"role": "assistant", "content": "model: first"} in second_call
    assert second_call[-1] == {"role": "user", "content": "second"}


def _command(text: str) -> UserCommand:
    return UserCommand(
        id=uuid4(),
        text=text,
        source="test",
        user_id="user-1",
        created_at=datetime.now(UTC),
    )
