import asyncio
from collections.abc import Callable, Iterator

import pytest

from app.cli import run
from app.core.command_bus import CommandBus
from app.llm.manager import LLMManager
from app.router.router import RuleBasedRouter
from app.workers.factory import WorkerFactory


class FakeLLMManager(LLMManager):
    def __init__(self) -> None:
        pass

    async def chat(self, text: str) -> str:
        return f"model: {text}"


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


def test_cli_prints_message_for_unimplemented_worker(
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

    assert "Worker is not implemented yet." in capsys.readouterr().out


def _read_input(user_input: Iterator[str]) -> Callable[[str], str]:
    def read_input(prompt: str = "") -> str:
        return next(user_input)

    return read_input
