from abc import ABC, abstractmethod

from app.domain.commands import UserCommand, WorkerResult


class BaseWorker(ABC):
    @abstractmethod
    def handle(self, command: UserCommand) -> WorkerResult:
        raise NotImplementedError
