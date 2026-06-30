from app.core.exceptions import LLMProviderError
from app.domain.commands import CommandResult, UserCommand
from app.llm.manager import LLMManager
from app.workers.base import BaseWorker


class EchoWorker(BaseWorker):
    def __init__(self, llm_manager: LLMManager) -> None:
        self._llm_manager = llm_manager

    async def handle(self, command: UserCommand) -> CommandResult:
        try:
            message = await self._llm_manager.chat(command.text)
        except LLMProviderError as exc:
            return CommandResult(success=False, message=str(exc))

        return CommandResult(success=True, message=message)
