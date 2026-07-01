import asyncio
from datetime import UTC, datetime
from uuid import uuid4

from app.core.command_bus import CommandBus
from app.domain.commands import UserCommand
from app.llm.manager import LLMManager
from app.router.router import RuleBasedRouter
from app.workers.factory import WorkerFactory


class FakeLLMManager(LLMManager):
    def __init__(self) -> None:
        pass

    async def chat(self, messages: list[dict[str, str]]) -> str:
        return f"model: {messages[-1]['content']}"


def test_command_bus_dispatches_command_to_echo_worker() -> None:
    command = UserCommand(
        id=uuid4(),
        text="hello",
        source="test",
        user_id="user-1",
        created_at=datetime.now(UTC),
    )
    bus = CommandBus(
        router=RuleBasedRouter(),
        worker_factory=WorkerFactory(llm_manager=FakeLLMManager()),
    )

    result = asyncio.run(bus.dispatch(command))

    assert result.success is True
    assert result.message == "model: hello"
    assert result.data == {}
