from datetime import UTC, datetime
from uuid import uuid4

from app.core.command_bus import CommandBus
from app.domain.commands import CommandResult, UserCommand


def test_user_command_can_be_created() -> None:
    command = UserCommand(
        id=uuid4(),
        text="hello",
        source="test",
        user_id="user-1",
        created_at=datetime.now(UTC),
    )

    assert command.text == "hello"
    assert command.metadata == {}


def test_command_result_can_be_created() -> None:
    result = CommandResult(success=True)

    assert result.success is True
    assert result.message is None
    assert result.data == {}


def test_command_bus_can_be_imported() -> None:
    assert CommandBus is not None
