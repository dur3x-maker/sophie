from app.domain.commands import CommandResult, UserCommand
from app.router.base import BaseRouter
from app.workers.factory import WorkerFactory


class CommandBus:
    def __init__(self, router: BaseRouter, worker_factory: WorkerFactory | None = None) -> None:
        self._router = router
        self._worker_factory = worker_factory or WorkerFactory()

    async def dispatch(self, command: UserCommand) -> CommandResult:
        worker_cls = self._router.route(command)
        worker = await self._worker_factory.create(worker_cls)
        return await worker.handle(command)
