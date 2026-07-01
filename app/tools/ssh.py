from importlib import import_module
from typing import Any

from app.core.logger import logger
from app.tools.base import BaseTool
from app.tools.result import ToolResult

ALLOWED_SSH_COMMANDS = frozenset(
    {
        "docker compose ps",
        "docker compose logs --tail=50",
        "uptime",
        "free -h",
        "df -h",
    }
)


class SSHTool(BaseTool):
    @property
    def name(self) -> str:
        return "ssh"

    @property
    def description(self) -> str:
        return "SSH remote command diagnostics tool."

    async def execute(self, **kwargs: Any) -> ToolResult:
        host = self._required_string(kwargs, "host")
        username = self._required_string(kwargs, "username")
        password = self._required_string(kwargs, "password")
        command = self._required_string(kwargs, "command")
        timeout = float(kwargs.get("timeout", 30.0))

        if command not in ALLOWED_SSH_COMMANDS:
            raise ValueError(f"Command is not allowed for SSHTool: {command}")

        logger.info(
            "Executing SSH diagnostic command on {host}: {command}", host=host, command=command
        )

        paramiko = import_module("paramiko")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(
                hostname=host,
                username=username,
                password=password,
                timeout=timeout,
                banner_timeout=timeout,
                auth_timeout=timeout,
            )
            _, stdout_stream, stderr_stream = client.exec_command(command, timeout=timeout)
            stdout = stdout_stream.read().decode("utf-8", errors="replace")
            stderr = stderr_stream.read().decode("utf-8", errors="replace")
            exit_code = int(stdout_stream.channel.recv_exit_status())
        finally:
            client.close()

        return ToolResult(
            success=exit_code == 0,
            output=stdout,
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            error=stderr or None,
            metadata={
                "host": host,
                "command": command,
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": exit_code,
            },
        )

    def _required_string(self, kwargs: dict[str, Any], key: str) -> str:
        value = kwargs.get(key)
        if not isinstance(value, str) or not value:
            raise ValueError(f"SSHTool requires {key}")
        return value
