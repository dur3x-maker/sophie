# Remote Infrastructure

## Status

Planned

## Goal

Sophie должна уметь безопасно подключаться к удалённому серверу и выполнять разрешённые диагностические команды.

## User Value

Пользователь сможет написать:

"Софи, проверь сервер"

и Sophie сможет подключиться по SSH, выполнить безопасные команды, вернуть результат и позже использовать это для DevOps-задач.

## Scope

Входит:

- SSH connection
- command execution
- stdout/stderr
- exit code
- timeout
- ToolResult
- security validation
- logs

Не входит:

- sudo
- passwords
- interactive shell
- file upload/download
- SCP/SFTP
- automatic destructive actions
- docker restart
- production auto-healing

## Tools

- SSHTool

## Workers

- DevOpsWorker

## Security Requirements

- только SSH key auth
- никаких паролей
- выполнение только через ToolExecutor
- SecurityValidator обязателен
- forbidden-команды блокируются до выполнения
- timeout обязателен
- все команды логируются
- destructive commands запрещены

## Milestones

1. SSHTool MVP
2. Remote command execution
3. DevOpsWorker integration
4. Docker diagnostics
5. Safe restart with confirmation

## Acceptance Criteria

Sophie умеет выполнить безопасную команду на удалённом сервере через SSH и вернуть ToolResult.
