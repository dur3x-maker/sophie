from abc import ABC, abstractmethod

from app.domain.commands import UserCommand


class BaseRouter(ABC):
    @abstractmethod
    def route(self, command: UserCommand) -> None:
        raise NotImplementedError
