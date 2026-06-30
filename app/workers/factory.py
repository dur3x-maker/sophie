from app.llm.manager import LLMManager
from app.workers.base import BaseWorker
from app.workers.echo import EchoWorker


class WorkerFactory:
    def __init__(self, llm_manager: LLMManager | None = None) -> None:
        self._llm_manager = llm_manager

    async def create(self, worker_cls: type[BaseWorker]) -> BaseWorker:
        if worker_cls is EchoWorker:
            if self._llm_manager is None:
                raise RuntimeError("LLMManager is required to create EchoWorker")
            return EchoWorker(llm_manager=self._llm_manager)

        return worker_cls()
