from dataclasses import dataclass
from enum import StrEnum


class RiskLevel(StrEnum):
    SAFE = "safe"
    CONFIRMATION_REQUIRED = "confirmation_required"
    FORBIDDEN = "forbidden"


@dataclass(frozen=True)
class SecurityPolicy:
    forbidden_patterns: tuple[str, ...] = (
        r"(^|[;&|]\s*)(sudo\s+)?rm\s+(?=[^;&|]*-[^\s]*r)(?=[^;&|]*-[^\s]*f)",
        r"(^|[;&|]\s*)(sudo\s+)?mkfs(?:\.|\s|$)",
        r"(^|[;&|]\s*)(sudo\s+)?shutdown(?:\s|$)",
        r"(^|[;&|]\s*)(sudo\s+)?reboot(?:\s|$)",
        r"(^|[;&|]\s*)(sudo\s+)?poweroff(?:\s|$)",
        r"(^|[;&|]\s*)(sudo\s+)?halt(?:\s|$)",
        r"(^|[;&|]\s*)(sudo\s+)?dd(?:\s|$)",
        r"(^|[;&|]\s*)(sudo\s+)?chmod\s+777\s+/(?:\s|$)",
        r"(^|[;&|]\s*)(sudo\s+)?chown\s+-r\s+/(?:\s|$)",
        r"(^|[;&|]\s*)sudo\s+su(?:\s|$)",
        r"(^|[;&|]\s*)(sudo\s+)?passwd(?:\s|$)",
        r"(^|[;&|]\s*)(sudo\s+)?userdel(?:\s|$)",
        r"(^|[;&|]\s*)(sudo\s+)?groupdel(?:\s|$)",
        r"(^|[;&|]\s*)(sudo\s+)?systemctl\s+poweroff(?:\s|$)",
        r"(^|[;&|]\s*)(sudo\s+)?systemctl\s+reboot(?:\s|$)",
    )
    dangerous_commands: tuple[str, ...] = (
        "rm -rf",
        "mkfs",
        "shutdown",
        "reboot",
        "poweroff",
        "halt",
        "dd",
        "chmod 777 /",
        "chown -R /",
        "sudo su",
        "passwd",
        "userdel",
        "groupdel",
        "systemctl poweroff",
        "systemctl reboot",
    )
    command_argument_names: tuple[str, ...] = (
        "command",
        "cmd",
        "shell_command",
    )
    default_risk_level: RiskLevel = RiskLevel.SAFE
