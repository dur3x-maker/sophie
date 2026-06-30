from app.workers.base import BaseWorker


class WorkerFactory:
    def create(self, worker_cls: type[BaseWorker]) -> BaseWorker:
        return worker_cls()
