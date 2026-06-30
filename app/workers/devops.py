from app.domain.commands import UserCommand, WorkerResult
from app.workers.base import BaseWorker


class DevOpsWorker(BaseWorker):
    def handle(self, command: UserCommand) -> WorkerResult:
        raise NotImplementedError
