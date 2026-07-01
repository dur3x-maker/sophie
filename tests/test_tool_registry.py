import asyncio
from typing import Any

import pytest

from app.tools.base import BaseTool
from app.tools.call import ToolCall
from app.tools.docker import DockerTool
from app.tools.echo import EchoTool
from app.tools.executor import ToolExecutor
from app.tools.filesystem import FilesystemTool
from app.tools.git import GitTool
from app.tools.http import HttpTool
from app.tools.manager import ToolManager
from app.tools.registry import ToolRegistry
from app.tools.result import ToolResult
from app.tools.shell import ShellTool
from app.tools.ssh import SSHTool


class FakeTool(BaseTool):
    @property
    def name(self) -> str:
        return "fake"

    @property
    def description(self) -> str:
        return "Fake test tool."

    async def execute(self, **kwargs: Any) -> ToolResult:
        return ToolResult(success=True, output="fake", metadata=kwargs)


class FailingTool(BaseTool):
    @property
    def name(self) -> str:
        return "failing"

    @property
    def description(self) -> str:
        return "Failing test tool."

    async def execute(self, **kwargs: Any) -> ToolResult:
        raise RuntimeError("boom")


def test_tool_registry_contains_default_tool_names() -> None:
    registry = ToolRegistry()

    assert registry.names() == ["ssh", "shell", "docker", "git", "filesystem", "http"]


def test_tool_registry_returns_default_tools() -> None:
    registry = ToolRegistry()

    assert isinstance(registry.get("ssh"), SSHTool)
    assert isinstance(registry.get("shell"), ShellTool)
    assert isinstance(registry.get("docker"), DockerTool)
    assert isinstance(registry.get("git"), GitTool)
    assert isinstance(registry.get("filesystem"), FilesystemTool)
    assert isinstance(registry.get("http"), HttpTool)


def test_tool_registry_returns_requested_tools_in_order() -> None:
    registry = ToolRegistry()

    tools = registry.get_many(["docker", "ssh"])

    assert [tool.name for tool in tools] == ["docker", "ssh"]


def test_tool_registry_creates_new_tool_instance() -> None:
    registry = ToolRegistry(tools=[FakeTool])

    assert registry.get("fake") is not registry.get("fake")


def test_tool_result_can_be_created() -> None:
    result = ToolResult(
        success=True,
        output="done",
        execution_time=0.1,
        metadata={"tool_name": "fake"},
    )

    assert result.success is True
    assert result.output == "done"
    assert result.error is None
    assert result.execution_time == 0.1
    assert result.metadata == {"tool_name": "fake"}


def test_tool_call_can_be_created() -> None:
    call = ToolCall(tool_name="echo", arguments={"value": "hello"})

    assert call.tool_name == "echo"
    assert call.arguments == {"value": "hello"}


def test_echo_tool_returns_tool_result() -> None:
    tool = EchoTool()
    result = asyncio.run(tool.execute())

    assert tool.requires_confirmation is False
    assert tool.risk_level == "safe"
    assert result == ToolResult(success=True, output="echo")


def test_tool_executor_returns_tool_result() -> None:
    result = asyncio.run(ToolExecutor().execute(EchoTool()))

    assert result.success is True
    assert result.output == "echo"
    assert result.execution_time > 0
    assert result.metadata == {"tool_name": "echo"}


def test_tool_executor_converts_tool_exception_to_result() -> None:
    result = asyncio.run(ToolExecutor().execute(FailingTool()))

    assert result.success is False
    assert result.output == ""
    assert result.error == "boom"
    assert result.execution_time > 0
    assert result.metadata == {
        "tool_name": "failing",
        "exception_type": "RuntimeError",
    }


def test_tool_manager_delegates_execution_to_registered_tool() -> None:
    manager = ToolManager(registry=ToolRegistry(tools=[EchoTool]))

    result = asyncio.run(manager.execute("echo", value=42))

    assert result.success is True
    assert result.output == "echo"
    assert result.metadata == {"tool_name": "echo"}


def test_tool_manager_returns_error_for_unknown_tool() -> None:
    manager = ToolManager(registry=ToolRegistry(tools=[EchoTool]))

    result = asyncio.run(manager.execute("unknown"))

    assert result == ToolResult(
        success=False,
        output="",
        error="Unknown tool: unknown",
        metadata={"tool_name": "unknown"},
    )


def test_tool_manager_returns_error_when_tool_raises() -> None:
    manager = ToolManager(registry=ToolRegistry(tools=[FailingTool]))

    result = asyncio.run(manager.execute("failing"))

    assert result.success is False
    assert result.error == "boom"
    assert result.metadata == {
        "tool_name": "failing",
        "exception_type": "RuntimeError",
    }


def test_tool_manager_handles_placeholder_tools() -> None:
    manager = ToolManager()

    result = asyncio.run(manager.execute("docker"))

    assert result.success is False
    assert result.error == "DockerTool is not implemented yet"
    assert result.metadata == {
        "tool_name": "docker",
        "exception_type": "NotImplementedError",
    }


def test_placeholder_tools_are_not_implemented() -> None:
    tool = DockerTool()

    with pytest.raises(NotImplementedError, match="DockerTool"):
        asyncio.run(tool.execute())
