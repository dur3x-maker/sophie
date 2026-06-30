from abc import ABC, abstractmethod

from app.domain.commands import CommandResult, UserCommand


class BaseWorker(ABC):
    @abstractmethod
    async def handle(self, command: UserCommand) -> CommandResult:
        raise NotImplementedError
