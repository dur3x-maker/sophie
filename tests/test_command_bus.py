from datetime import UTC, datetime
from uuid import uuid4

from app.core.command_bus import CommandBus
from app.domain.commands import UserCommand
from app.router.router import RuleBasedRouter


def test_command_bus_dispatches_command_to_echo_worker() -> None:
    command = UserCommand(
        id=uuid4(),
        text="Привет",
        source="test",
        user_id="user-1",
        created_at=datetime.now(UTC),
    )
    bus = CommandBus(router=RuleBasedRouter())

    result = bus.dispatch(command)

    assert result.success is True
    assert result.message == "Привет"
    assert result.data == {}
