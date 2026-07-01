import asyncio
from typing import Any

import pytest

from app.security.exceptions import SecurityViolation
from app.security.policy import RiskLevel, SecurityPolicy
from app.security.validator import SecurityValidator
from app.tools.base import BaseTool
from app.tools.executor import ToolExecutor
from app.tools.result import ToolResult


class RecordingCommandTool(BaseTool):
    def __init__(self) -> None:
        self.was_called = False

    @property
    def name(self) -> str:
        return "recording"

    @property
    def description(self) -> str:
        return "Records whether execute was called."

    async def execute(self, **kwargs: Any) -> ToolResult:
        self.was_called = True
        return ToolResult(success=True, output="ok")


@pytest.mark.parametrize(
    "command",
    [
        "rm -rf /",
        "rm -r -f /",
        "sudo rm -rf /",
        "shutdown",
        "reboot",
        "dd if=/dev/zero of=/dev/sda",
        "mkfs.ext4 /dev/sda1",
    ],
)
def test_security_validator_rejects_forbidden_commands(command: str) -> None:
    validator = SecurityValidator()

    with pytest.raises(SecurityViolation):
        validator.validate(command)


@pytest.mark.parametrize("command", ["docker ps", "pwd", "ls"])
def test_security_validator_allows_safe_commands(command: str) -> None:
    SecurityValidator().validate(command)


def test_security_policy_exposes_risk_levels_and_rules() -> None:
    policy = SecurityPolicy()

    assert policy.default_risk_level is RiskLevel.SAFE
    assert RiskLevel.CONFIRMATION_REQUIRED.value == "confirmation_required"
    assert RiskLevel.FORBIDDEN.value == "forbidden"
    assert "rm -rf" in policy.dangerous_commands


def test_tool_executor_blocks_forbidden_command_before_tool_execution() -> None:
    tool = RecordingCommandTool()
    result = asyncio.run(ToolExecutor().execute(tool, command="rm -rf /"))

    assert tool.was_called is False
    assert result.success is False
    assert result.output == ""
    assert result.error == "Forbidden command rejected: rm -rf /"
    assert result.metadata == {
        "tool_name": "recording",
        "exception_type": "SecurityViolation",
    }


def test_tool_executor_validates_common_command_argument_aliases() -> None:
    tool = RecordingCommandTool()
    result = asyncio.run(ToolExecutor().execute(tool, cmd="shutdown"))

    assert tool.was_called is False
    assert result.success is False
    assert result.error == "Forbidden command rejected: shutdown"
