import asyncio
from collections.abc import Callable, Iterator

import pytest

from app.cli import run


def test_cli_prints_echo_result(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    user_input = iter(("привет", "exit"))

    monkeypatch.setattr("builtins.input", _read_input(user_input))

    asyncio.run(run())

    assert "привет" in capsys.readouterr().out


def test_cli_prints_message_for_unimplemented_worker(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    user_input = iter(("напиши пост", "exit"))

    monkeypatch.setattr("builtins.input", _read_input(user_input))

    asyncio.run(run())

    assert "Worker is not implemented yet." in capsys.readouterr().out


def _read_input(user_input: Iterator[str]) -> Callable[[str], str]:
    def read_input(prompt: str = "") -> str:
        return next(user_input)

    return read_input
