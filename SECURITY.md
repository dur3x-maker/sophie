# Security Policy

Sophie is designed so that the LLM never receives direct access to the host system,
remote servers, shells, Docker daemons, Git repositories, or filesystems.

The LLM may suggest an action only as structured data. Execution is controlled by the
application.

Allowed execution path:

```text
AgentLoop
    -> ToolManager
    -> ToolExecutor
    -> Tool
```

No Worker, Planner, Provider, or LLM response may bypass this path.

## Core Rules

- LLM output is untrusted input.
- LLM never calls a Tool directly.
- Workers never execute shell, SSH, Docker, Git, or filesystem operations directly.
- Tool execution must go through `ToolExecutor`.
- `ToolExecutor` is the security gate before a Tool can run.
- Destructive commands must be rejected even if the LLM or user requests them.
- Future remote tools must validate command-like input before execution.

## Forbidden Commands

The following commands and any analogous destructive command are forbidden:

- `rm -rf`
- `mkfs`
- `shutdown`
- `reboot`
- `poweroff`
- `halt`
- `dd`
- `chmod 777 /`
- `chown -R /`
- `sudo su`
- `passwd`
- `userdel`
- `groupdel`
- `systemctl poweroff`
- `systemctl reboot`

These commands must not be executed through Sophie.

## Trust Levels

The security layer defines three risk levels:

- `SAFE`
- `CONFIRMATION_REQUIRED`
- `FORBIDDEN`

Current implementation uses `FORBIDDEN` checks for command validation. Confirmation
flows are reserved for future work.

## Current Scope

This security foundation does not implement SSH, Docker, Git, Shell, Filesystem, or HTTP
execution. It only defines the policy and validation architecture that future remote
tools must use.
