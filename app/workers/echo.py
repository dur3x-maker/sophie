from app.domain.commands import CommandResult, UserCommand
from app.workers.base import BaseWorker


class EchoWorker(BaseWorker):
    async def handle(self, command: UserCommand) -> CommandResult:
        return CommandResult(success=True, message=command.text)
