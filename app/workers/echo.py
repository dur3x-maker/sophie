from app.core.exceptions import LLMProviderError
from app.domain.commands import CommandResult, UserCommand
from app.llm.manager import LLMManager
from app.workers.base import BaseWorker

LLM_FALLBACK_MESSAGE = (
    "Я уже на связи, но LLM пока не подключена. "
    "Проверь OPENROUTER_API_KEY и OPENROUTER_MODEL в .env."
)


class EchoWorker(BaseWorker):
    def __init__(self, llm_manager: LLMManager) -> None:
        self._llm_manager = llm_manager

    async def handle(self, command: UserCommand) -> CommandResult:
        try:
            message = await self._llm_manager.chat(command.text)
        except LLMProviderError:
            return CommandResult(success=False, message=LLM_FALLBACK_MESSAGE)

        return CommandResult(success=True, message=message)
