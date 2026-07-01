import asyncio
from typing import Any

import pytest

from app.tools.base import BaseTool
from app.tools.docker import DockerTool
from app.tools.filesystem import FilesystemTool
from app.tools.git import GitTool
from app.tools.http import HttpTool
from app.tools.manager import ToolManager
from app.tools.registry import ToolRegistry
from app.tools.shell import ShellTool
from app.tools.ssh import SSHTool


class FakeTool(BaseTool):
    def name(self) -> str:
        return "fake"

    def description(self) -> str:
        return "Fake test tool."

    async def execute(self, **kwargs: Any) -> Any:
        return kwargs


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

    assert [tool.name() for tool in tools] == ["docker", "ssh"]


def test_tool_manager_delegates_execution_to_registered_tool() -> None:
    manager = ToolManager(registry=ToolRegistry(tools=[FakeTool()]))

    result = asyncio.run(manager.execute("fake", value=42))

    assert result == {"value": 42}


def test_placeholder_tools_are_not_implemented() -> None:
    tool = DockerTool()

    with pytest.raises(NotImplementedError, match="DockerTool"):
        asyncio.run(tool.execute())
