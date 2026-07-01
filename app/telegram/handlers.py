from datetime import UTC, datetime
from typing import Any, Protocol
from uuid import uuid4

from aiogram import F, Router
from aiogram.types import Message, User

from app.core.command_bus import CommandBus
from app.core.logger import logger
from app.domain.commands import CommandResult, UserCommand

router = Router()


class CommandDispatcher(Protocol):
    async def dispatch(self, command: UserCommand) -> CommandResult: ...


class ReplyMessage(Protocol):
    text: str | None
    from_user: User | None

    def answer(self, text: str) -> Any: ...


def build_user_command(message: ReplyMessage) -> UserCommand:
    user_id = str(message.from_user.id) if message.from_user is not None else "unknown"
    chat = getattr(message, "chat", None)
    chat_id = str(chat.id) if chat is not None else user_id

    return UserCommand(
        id=uuid4(),
        text=message.text or "",
        source="telegram",
        user_id=user_id,
        created_at=datetime.now(UTC),
        metadata={"chat_id": chat_id},
    )


@router.message(F.text)
async def handle_text_message(message: Message, command_bus: CommandBus) -> None:
    await process_text_message(message, command_bus)


async def process_text_message(message: ReplyMessage, command_bus: CommandDispatcher) -> None:
    logger.info("Received Telegram message")

    try:
        result = await command_bus.dispatch(build_user_command(message))
    except Exception as exc:
        logger.exception("Telegram message processing failed")
        await message.answer(f"Error: {exc}")
        return

    await message.answer(result.message or "")
    logger.info("Telegram message processed")
