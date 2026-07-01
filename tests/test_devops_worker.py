import asyncio
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.config.settings import Settings
from app.devops.server_registry import ServerRegistry
from app.domain.commands import UserCommand
from app.llm.manager import LLMManager
from app.llm.model_registry import ModelRegistry
from app.llm.prompt_builder import PromptBuilder
from app.memory.in_memory import InMemoryConversationMemory
from app.tools.base import BaseTool
from app.tools.registry import ToolRegistry
from app.tools.result import ToolResult
from app.workers.devops import DevOpsWorker
from app.workers.factory import WorkerFactory


class FakeLLMManager(LLMManager):
    def __init__(self) -> None:
        self.messages: list[list[dict[str, str]]] = []

    async def chat(self, messages: list[dict[str, str]]) -> str:
        self.messages.append(messages)
        return "Контейнеры работают. Backend healthy. Ошибок не обнаружено."


class FakeSSHTool(BaseTool):
    calls: list[dict[str, Any]] = []

    @property
    def name(self) -> str:
        return "ssh"

    @property
    def description(self) -> str:
        return "Fake SSH tool."

    async def execute(self, **kwargs: Any) -> ToolResult:
        self.calls.append(kwargs)
        command = kwargs["command"]
        if command == "docker compose ps":
            output = "backend running healthy"
        else:
            output = "backend no errors"

        return ToolResult(
            success=True,
            output=output,
            stdout=output,
            stderr="",
            exit_code=0,
            metadata={
                "stdout": output,
                "stderr": "",
                "exit_code": 0,
            },
        )


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
    assert [tool.name for tool in worker.allowed_tools] == ["ssh"]


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


def test_devops_worker_runs_docker_diagnostics_on_known_server() -> None:
    FakeSSHTool.calls = []
    llm_manager = FakeLLMManager()
    worker = DevOpsWorker(
        llm_manager=llm_manager,
        memory=InMemoryConversationMemory(),
        prompt_builder=PromptBuilder(),
        tool_registry=ToolRegistry(tools=[FakeSSHTool]),
        server_registry=ServerRegistry(settings=_settings()),
    )

    result = asyncio.run(worker.handle(_command("Что с докером на Швеции?")))

    assert result.success is True
    assert result.message == "Контейнеры работают. Backend healthy. Ошибок не обнаружено."
    assert [call["command"] for call in FakeSSHTool.calls] == [
        "docker compose ps",
        "docker compose logs --tail=50",
    ]
    assert {call["host"] for call in FakeSSHTool.calls} == {"sweden.example.com"}
    assert "backend running healthy" in llm_manager.messages[0][-1]["content"]
    assert "backend no errors" in llm_manager.messages[0][-1]["content"]


def _settings() -> Settings:
    return Settings(
        server_sweden_host="sweden.example.com",
        server_sweden_username="deploy",
        server_sweden_password="secret",
        server_france_host="france.example.com",
        server_france_username="deploy",
        server_france_password="secret",
        server_usa_host="usa.example.com",
        server_usa_username="deploy",
        server_usa_password="secret",
    )


def _command(text: str) -> UserCommand:
    return UserCommand(
        id=uuid4(),
        text=text,
        source="test",
        user_id="user-1",
        created_at=datetime.now(UTC),
    )
