import asyncio

from app.config.settings import get_settings
from app.core.command_bus import CommandBus
from app.core.logger import logger
from app.llm.manager import LLMManager
from app.providers.openrouter import OpenRouterProvider
from app.router.router import RuleBasedRouter
from app.telegram.bot import create_bot, create_dispatcher, start_bot
from app.workers.factory import WorkerFactory


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


async def run() -> None:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required")

    bot = create_bot(settings.telegram_bot_token)
    dispatcher = create_dispatcher()
    command_bus = build_command_bus()

    try:
        await start_bot(bot=bot, dispatcher=dispatcher, command_bus=command_bus)
    except Exception:
        logger.exception("Telegram bot failed")
        raise
    finally:
        await bot.session.close()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
