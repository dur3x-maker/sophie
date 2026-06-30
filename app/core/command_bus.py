from app.domain.commands import UserCommand, WorkerResult
from app.router.base import BaseRouter
from app.workers.factory import WorkerFactory


class CommandBus:
    def __init__(self, router: BaseRouter, worker_factory: WorkerFactory | None = None) -> None:
        self._router = router
        self._worker_factory = worker_factory or WorkerFactory()

    def dispatch(self, command: UserCommand) -> WorkerResult:
        worker_cls = self._router.route(command)
        worker = self._worker_factory.create(worker_cls)
        return worker.handle(command)
