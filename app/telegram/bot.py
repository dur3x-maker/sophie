from aiogram import Bot, Dispatcher

from app.core.command_bus import CommandBus
from app.core.logger import logger
from app.telegram.handlers import router


def create_bot(token: str) -> Bot:
    return Bot(token=token)


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    return dispatcher


async def start_bot(bot: Bot, dispatcher: Dispatcher, command_bus: CommandBus) -> None:
    logger.info("Telegram bot started")
    await dispatcher.start_polling(bot, command_bus=command_bus)
