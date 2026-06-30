from app.domain.commands import CommandResult, UserCommand
from app.workers.base import BaseWorker


class MarketingWorker(BaseWorker):
    async def handle(self, command: UserCommand) -> CommandResult:
        raise NotImplementedError
