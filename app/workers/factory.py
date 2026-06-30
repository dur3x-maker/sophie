from app.workers.base import BaseWorker


class WorkerFactory:
    async def create(self, worker_cls: type[BaseWorker]) -> BaseWorker:
        return worker_cls()
