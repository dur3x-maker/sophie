from app.domain.commands import UserCommand
from app.router.base import BaseRouter


class CommandBus:
    def __init__(self, router: BaseRouter) -> None:
        self._router = router

    def dispatch(self, command: UserCommand) -> None:
        raise NotImplementedError
