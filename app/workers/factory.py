from app.llm.manager import LLMManager
from app.llm.model_registry import ModelRegistry
from app.llm.prompt_builder import PromptBuilder
from app.memory.base import BaseMemory
from app.memory.in_memory import InMemoryConversationMemory
from app.tools.registry import ToolRegistry
from app.workers.base import BaseWorker
from app.workers.devops import DevOpsWorker
from app.workers.llm_conversation import LLMConversationWorker


class WorkerFactory:
    def __init__(
        self,
        llm_manager: LLMManager | None = None,
        memory: BaseMemory | None = None,
        prompt_builder: PromptBuilder | None = None,
        model_registry: ModelRegistry | None = None,
        tool_registry: ToolRegistry | None = None,
    ) -> None:
        self._llm_manager = llm_manager
        self._memory = memory or InMemoryConversationMemory()
        self._prompt_builder = prompt_builder or PromptBuilder()
        self._model_registry = model_registry or ModelRegistry()
        self._tool_registry = tool_registry or ToolRegistry()

    async def create(self, worker_cls: type[BaseWorker]) -> BaseWorker:
        if issubclass(worker_cls, LLMConversationWorker):
            if self._llm_manager is None:
                raise RuntimeError("LLMManager is required to create LLM conversation worker")
            if worker_cls is DevOpsWorker:
                return DevOpsWorker(
                    llm_manager=self._llm_manager,
                    memory=self._memory,
                    prompt_builder=self._prompt_builder,
                    model_registry=self._model_registry,
                    tool_registry=self._tool_registry,
                )
            return worker_cls(
                llm_manager=self._llm_manager,
                memory=self._memory,
                prompt_builder=self._prompt_builder,
            )

        return worker_cls()
