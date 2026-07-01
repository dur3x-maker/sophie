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


class FakeDockerHealthTool(BaseTool):
    calls: list[dict[str, Any]] = []

    @property
    def name(self) -> str:
        return "docker_health"

    @property
    def description(self) -> str:
        return "Fake Docker health tool."

    async def execute(self, **kwargs: Any) -> ToolResult:
        self.calls.append(kwargs)
        return ToolResult(
            success=True,
            output="docker healthy",
            metadata={"ps": "backend running healthy", "logs": "backend no errors"},
        )


class FakeServerInfoTool(BaseTool):
    calls: list[dict[str, Any]] = []

    @property
    def name(self) -> str:
        return "server_info"

    @property
    def description(self) -> str:
        return "Fake server info tool."

    async def execute(self, **kwargs: Any) -> ToolResult:
        self.calls.append(kwargs)
        return ToolResult(
            success=True,
            output="server ok",
            metadata={"uptime": "up 10 days", "memory": "free", "disk": "ok"},
        )


def test_devops_worker_configuration_uses_registries() -> None:
    worker = DevOpsWorker(
        llm_manager=FakeLLMManager(),
        memory=InMemoryConversationMemory(),
        prompt_builder=PromptBuilder(),
        model_registry=ModelRegistry(worker_models={"devops": "custom/devops"}),
        tool_registry=ToolRegistry(tools=[FakeDockerHealthTool, FakeServerInfoTool]),
    )

    assert worker.prompt_path == "app/prompts/workers/devops.md"
    assert worker.model == "custom/devops"
    assert [tool.name for tool in worker.allowed_tools] == ["docker_health", "server_info"]


def test_worker_factory_injects_devops_worker_configuration() -> None:
    worker = asyncio.run(
        WorkerFactory(
            llm_manager=FakeLLMManager(),
            model_registry=ModelRegistry(worker_models={"devops": "custom/devops"}),
            tool_registry=ToolRegistry(tools=[FakeDockerHealthTool, FakeServerInfoTool]),
        ).create(DevOpsWorker)
    )

    assert isinstance(worker, DevOpsWorker)
    assert worker.model == "custom/devops"
    assert [tool.name for tool in worker.allowed_tools] == list(DevOpsWorker.allowed_tool_names)


def test_devops_worker_runs_docker_diagnostics_on_known_server() -> None:
    FakeDockerHealthTool.calls = []
    llm_manager = FakeLLMManager()
    worker = DevOpsWorker(
        llm_manager=llm_manager,
        memory=InMemoryConversationMemory(),
        prompt_builder=PromptBuilder(),
        tool_registry=ToolRegistry(tools=[FakeDockerHealthTool, FakeServerInfoTool]),
        server_registry=ServerRegistry(settings=_settings()),
    )

    result = asyncio.run(worker.handle(_command("Что с докером на Швеции?")))

    assert result.success is True
    assert result.message == "Контейнеры работают. Backend healthy. Ошибок не обнаружено."
    assert len(FakeDockerHealthTool.calls) == 1
    assert FakeDockerHealthTool.calls[0]["host"] == "sweden.example.com"
    assert "docker_health" in llm_manager.messages[0][-1]["content"]
    assert "backend running healthy" in llm_manager.messages[0][-1]["content"]
    assert "backend no errors" in llm_manager.messages[0][-1]["content"]


def test_devops_worker_runs_server_info_on_known_server() -> None:
    FakeServerInfoTool.calls = []
    llm_manager = FakeLLMManager()
    worker = DevOpsWorker(
        llm_manager=llm_manager,
        memory=InMemoryConversationMemory(),
        prompt_builder=PromptBuilder(),
        tool_registry=ToolRegistry(tools=[FakeDockerHealthTool, FakeServerInfoTool]),
        server_registry=ServerRegistry(settings=_settings()),
    )

    result = asyncio.run(worker.handle(_command("Как там Франция?")))

    assert result.success is True
    assert len(FakeServerInfoTool.calls) == 1
    assert FakeServerInfoTool.calls[0]["host"] == "france.example.com"
    assert "server_info" in llm_manager.messages[0][-1]["content"]
    assert "up 10 days" in llm_manager.messages[0][-1]["content"]


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
