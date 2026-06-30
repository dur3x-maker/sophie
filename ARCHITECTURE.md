# Sophie Architecture

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
