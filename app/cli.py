import asyncio
from contextlib import suppress
from datetime import UTC, datetime
from uuid import uuid4

from app.core.command_bus import CommandBus
from app.domain.commands import UserCommand
from app.router.router import RuleBasedRouter
from app.workers.factory import WorkerFactory


def build_command(text: str) -> UserCommand:
    return UserCommand(
        id=uuid4(),
        text=text,
        source="cli",
        user_id="local",
        created_at=datetime.now(UTC),
    )


async def run() -> None:
    bus = CommandBus(router=RuleBasedRouter(), worker_factory=WorkerFactory())
    exit_commands = {"exit", "quit", "выход"}

    while True:
        try:
            text = input("> ").strip()
        except EOFError:
            break

        if not text:
            continue
        if text.lower() in exit_commands:
            break

        try:
            result = await bus.dispatch(build_command(text))
        except NotImplementedError:
            print("Worker is not implemented yet.")
            continue

        if result.message is not None:
            print(result.message)


def main() -> None:
    with suppress(KeyboardInterrupt):
        asyncio.run(run())


if __name__ == "__main__":
    main()
