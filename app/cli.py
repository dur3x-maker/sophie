import asyncio
from contextlib import suppress
from datetime import UTC, datetime
from uuid import uuid4

from app.config.settings import get_settings
from app.core.command_bus import CommandBus
from app.domain.commands import UserCommand
from app.llm.manager import LLMManager
from app.providers.openrouter import OpenRouterProvider
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


def build_command_bus() -> CommandBus:
    settings = get_settings()
    provider = OpenRouterProvider(
        api_key=settings.openrouter_api_key or "",
        model=settings.openrouter_model or "",
        base_url=settings.openrouter_base_url,
    )
    llm_manager = LLMManager(provider=provider)
    worker_factory = WorkerFactory(llm_manager=llm_manager)
    return CommandBus(router=RuleBasedRouter(), worker_factory=worker_factory)


async def run(bus: CommandBus | None = None) -> None:
    command_bus = bus or build_command_bus()
    exit_commands = {"exit", "quit", "\u0432\u044b\u0445\u043e\u0434"}

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
            result = await command_bus.dispatch(build_command(text))
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
