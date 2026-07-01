import asyncio
from collections.abc import Callable, Iterator

import pytest

from app.cli import run
from app.core.command_bus import CommandBus
from app.core.exceptions import LLMProviderError
from app.llm.manager import LLMManager
from app.router.router import RuleBasedRouter
from app.workers.echo import LLM_FALLBACK_MESSAGE
from app.workers.factory import WorkerFactory


class FakeLLMManager(LLMManager):
    def __init__(self) -> None:
        pass

    async def chat(self, messages: list[dict[str, str]]) -> str:
        return f"model: {messages[-1]['content']}"


class FailingLLMManager(LLMManager):
    def __init__(self) -> None:
        pass

    async def chat(self, messages: list[dict[str, str]]) -> str:
        raise LLMProviderError("provider failed")


def test_cli_prints_echo_result(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    user_input = iter(("hello", "exit"))
    bus = CommandBus(
        router=RuleBasedRouter(),
        worker_factory=WorkerFactory(llm_manager=FakeLLMManager()),
    )

    monkeypatch.setattr("builtins.input", _read_input(user_input))

    asyncio.run(run(bus=bus))

    assert "model: hello" in capsys.readouterr().out


def test_cli_prints_fallback_when_llm_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    user_input = iter(("hello", "exit"))
    bus = CommandBus(
        router=RuleBasedRouter(),
        worker_factory=WorkerFactory(llm_manager=FailingLLMManager()),
    )

    monkeypatch.setattr("builtins.input", _read_input(user_input))

    asyncio.run(run(bus=bus))

    assert LLM_FALLBACK_MESSAGE in capsys.readouterr().out


def test_cli_routes_specialized_worker_to_llm_pipeline(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    user_input = iter(("write post", "exit"))
    bus = CommandBus(
        router=RuleBasedRouter(),
        worker_factory=WorkerFactory(llm_manager=FakeLLMManager()),
    )

    monkeypatch.setattr("builtins.input", _read_input(user_input))

    asyncio.run(run(bus=bus))

    assert "model: write post" in capsys.readouterr().out


def _read_input(user_input: Iterator[str]) -> Callable[[str], str]:
    def read_input(prompt: str = "") -> str:
        return next(user_input)

    return read_input
