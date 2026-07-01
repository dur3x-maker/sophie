import asyncio

from app.llm.manager import LLMManager
from app.llm.model_registry import ModelRegistry
from app.llm.prompt_builder import PromptBuilder
from app.memory.in_memory import InMemoryConversationMemory
from app.tools.registry import ToolRegistry
from app.workers.devops import DevOpsWorker
from app.workers.factory import WorkerFactory


class FakeLLMManager(LLMManager):
    def __init__(self) -> None:
        pass

    async def chat(self, messages: list[dict[str, str]]) -> str:
        return "ok"


def test_devops_worker_configuration_uses_registries() -> None:
    worker = DevOpsWorker(
        llm_manager=FakeLLMManager(),
        memory=InMemoryConversationMemory(),
        prompt_builder=PromptBuilder(),
        model_registry=ModelRegistry(worker_models={"devops": "custom/devops"}),
        tool_registry=ToolRegistry(),
    )

    assert worker.prompt_path == "app/prompts/workers/devops.md"
    assert worker.model == "custom/devops"
    assert [tool.name for tool in worker.allowed_tools] == [
        "ssh",
        "shell",
        "docker",
        "git",
        "filesystem",
        "http",
    ]


def test_worker_factory_injects_devops_worker_configuration() -> None:
    worker = asyncio.run(
        WorkerFactory(
            llm_manager=FakeLLMManager(),
            model_registry=ModelRegistry(worker_models={"devops": "custom/devops"}),
            tool_registry=ToolRegistry(),
        ).create(DevOpsWorker)
    )

    assert isinstance(worker, DevOpsWorker)
    assert worker.model == "custom/devops"
    assert [tool.name for tool in worker.allowed_tools] == list(DevOpsWorker.allowed_tool_names)
