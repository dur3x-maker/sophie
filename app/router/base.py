from abc import ABC, abstractmethod

from app.domain.commands import UserCommand
from app.workers.base import BaseWorker


class BaseRouter(ABC):
    @abstractmethod
    def route(self, command: UserCommand) -> type[BaseWorker]:
        raise NotImplementedError
