# Contributing

## Commit Style

Используется Conventional Commits:

- `feat:` — новая возможность.
- `fix:` — исправление ошибки.
- `refactor:` — изменение структуры без изменения поведения.
- `test:` — тесты.
- `docs:` — документация.
- `chore:` — обслуживание проекта.

## Naming

- Python modules: `snake_case`.
- Classes: `PascalCase`.
- Functions and variables: `snake_case`.
- Tests: `test_<behavior>.py`.
- Abstract contracts: `Base<Name>`.

## Tests

- Каждый новый модуль должен иметь собственные тесты.
- Тесты не должны обращаться к реальным LLM providers, Telegram API или внешним сервисам.
- Для внешних зависимостей используются fake implementations.
- Перед commit должны проходить `pytest`, `ruff check`, `ruff format --check`, `mypy`.

## Pull Requests

PR должен содержать:

- краткое описание задачи;
- список измененных областей;
- результат проверок;
- архитектурные замечания, если они есть;
- Self Review.

## Development Process

1. Прочитать задачу.
2. Проверить текущие контракты.
3. Реализовать минимальное изменение.
4. Добавить или обновить тесты.
5. Запустить проверки.
6. Выполнить Self Review.
7. Создать commit и push.

## Architecture Changes

Самостоятельные архитектурные изменения запрещены. Если задача требует изменения pipeline, контракта или границы слоя, разработчик должен остановиться, описать проблему и дождаться решения Tech Lead.
