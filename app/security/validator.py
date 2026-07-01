import re

from app.security.exceptions import SecurityViolation
from app.security.policy import SecurityPolicy


class SecurityValidator:
    def __init__(self, policy: SecurityPolicy | None = None) -> None:
        self._policy = policy or SecurityPolicy()

    def validate(self, command: str) -> None:
        normalized_command = self._normalize(command)

        for pattern in self._policy.forbidden_patterns:
            if re.search(pattern, normalized_command, flags=re.IGNORECASE):
                raise SecurityViolation(f"Forbidden command rejected: {command}")

    def _normalize(self, command: str) -> str:
        return " ".join(command.strip().split()).lower()
