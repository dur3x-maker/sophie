# Sophie Architecture

## Capability-based Development

New Sophie features are added through capabilities. A capability must describe real
user value: what Sophie can do for the user, which tools and workers are involved,
which prompts, tests, and docs are required, and what acceptance criteria prove the
ability works.

Capabilities may include Tools, Workers, Prompts, Tests, and Docs. New abstract
architecture layers are not added unless a capability needs them.

## Security Layer

LLM output is untrusted. The LLM does not receive direct access to the host system or
remote infrastructure and does not call tools by itself.

Tool execution must follow one path:

```text
AgentLoop
        ↓
ToolManager
        ↓
ToolExecutor
        ↓
Tool
```

`ToolExecutor` owns the security gate for command-like tool arguments through
`SecurityValidator`. Security rules live in `SecurityPolicy`, not inside workers or
individual tools.

## Назначение проекта

Sophie — платформа персонального AI-агента. Проект строится вокруг единого pipeline обработки пользовательских команд, чтобы разные интерфейсы могли использовать одну и ту же доменную модель.

## Архитектурные принципы

- Interfaces не содержат бизнес-логики.
- CommandBus координирует выполнение.
- Router только выбирает Worker.
- Worker выполняет задачу.
- Все обращения к LLM проходят только через LLMManager.
- Все обращения к внешним сервисам должны проходить только через Tools.
- Memory является отдельным слоем.
- Архитектура считается замороженной и изменяется только после решения Tech Lead.

## Pipeline

```text
CLI / Telegram / API
        ↓
UserCommand
        ↓
CommandBus
        ↓
Router
        ↓
WorkerFactory
        ↓
Worker
        ↓
LLMManager / Tools / Memory
        ↓
CommandResult
```

## Dependency Rules

- Worker не знает про Telegram, CLI или API.
- Router не знает про LLM, Tools или Memory.
- Interfaces не знают про конкретные Worker.
- Provider не знает про Router, CommandBus или Interfaces.
- LLM вызывается только через LLMManager.
- Memory не подключается к PostgreSQL или Redis в текущей in-memory реализации.
- Worker взаимодействует только с разрешенными слоями.

## Структура проекта

- `app/api/` — будущий HTTP/API интерфейс.
- `app/config/` — настройки приложения через `pydantic-settings`.
- `app/core/` — инфраструктурное ядро: CommandBus, logger, lifecycle, exceptions.
- `app/domain/` — доменные модели, включая `UserCommand` и `CommandResult`.
- `app/llm/` — LLMManager и будущие LLM-схемы.
- `app/memory/` — контракты и реализации памяти.
- `app/planner/` — будущий слой планирования.
- `app/providers/` — провайдеры LLM, включая OpenRouter.
- `app/router/` — контракт Router и rule-based реализация.
- `app/telegram/` — Telegram interface на aiogram.
- `app/tools/` — будущие интеграции с внешними сервисами.
- `app/workers/` — контракты, registry, factory и реализации Worker.
- `tests/` — тесты контракта, pipeline, интерфейсов и отдельных модулей.
- `docker/` — директория для Docker-related файлов.

## Правила разработки

Порядок работы:

1. Контракт.
2. Реализация.
3. Тест.
4. Интеграция.

Новые возможности добавляются без архитектурных рефакторингов. Если задача требует изменения контракта или pipeline, нужно остановиться и дождаться решения Tech Lead.
