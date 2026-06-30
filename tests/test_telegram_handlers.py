import asyncio
from dataclasses import dataclass

from aiogram.types import User

from app.core.command_bus import CommandBus
from app.core.exceptions import LLMProviderError
from app.domain.commands import CommandResult, UserCommand
from app.llm.manager import LLMManager
from app.router.router import RuleBasedRouter
from app.telegram.handlers import build_user_command, process_text_message
from app.workers.echo import LLM_FALLBACK_MESSAGE
from app.workers.factory import WorkerFactory


@dataclass
class FakeMessage:
    text: str | None
    from_user: User | None
    answers: list[str]

    async def answer(self, text: str) -> object:
        self.answers.append(text)
        return None


class FakeCommandBus:
    def __init__(self, result: CommandResult | None = None, error: Exception | None = None) -> None:
        self._result = result
        self._error = error
        self.command: UserCommand | None = None

    async def dispatch(self, command: UserCommand) -> CommandResult:
        self.command = command
        if self._error is not None:
            raise self._error
        return self._result or CommandResult(success=True, message="ok")


class FailingLLMManager(LLMManager):
    def __init__(self) -> None:
        pass

    async def chat(self, text: str) -> str:
        raise LLMProviderError("provider failed")


def test_build_user_command_from_telegram_message() -> None:
    message = FakeMessage(
        text="hello",
        from_user=User(id=123, is_bot=False, first_name="Test"),
        answers=[],
    )

    command = build_user_command(message)

    assert command.text == "hello"
    assert command.source == "telegram"
    assert command.user_id == "123"


def test_process_text_message_answers_with_command_result() -> None:
    message = FakeMessage(
        text="hello",
        from_user=User(id=123, is_bot=False, first_name="Test"),
        answers=[],
    )
    command_bus = FakeCommandBus(result=CommandResult(success=True, message="hi"))

    asyncio.run(process_text_message(message, command_bus))

    assert message.answers == ["hi"]
    assert command_bus.command is not None
    assert command_bus.command.text == "hello"


def test_process_text_message_answers_with_error_message() -> None:
    message = FakeMessage(
        text="hello",
        from_user=User(id=123, is_bot=False, first_name="Test"),
        answers=[],
    )
    command_bus = FakeCommandBus(error=RuntimeError("failed"))

    asyncio.run(process_text_message(message, command_bus))

    assert message.answers == ["Error: failed"]


def test_telegram_pipeline_answers_with_fallback_when_llm_is_unavailable() -> None:
    message = FakeMessage(
        text="hello",
        from_user=User(id=123, is_bot=False, first_name="Test"),
        answers=[],
    )
    command_bus = CommandBus(
        router=RuleBasedRouter(),
        worker_factory=WorkerFactory(llm_manager=FailingLLMManager()),
    )

    asyncio.run(process_text_message(message, command_bus))

    assert message.answers == [LLM_FALLBACK_MESSAGE]
