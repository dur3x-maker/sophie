# Sophie

## Remote Infrastructure Diagnostics

Пример 1:

```text
Пользователь: Что с докером на Швеции?
Sophie: DockerHealthTool -> краткая человеческая выжимка.
```

Пример 2:

```text
Пользователь: Как там Франция?
Sophie: ServerInfoTool -> краткая человеческая выжимка.
```

## Remote Infrastructure Example

Пользователь:

```text
Что с докером на Франции?
```

Sophie:

```text
Контейнеры работают.
Backend healthy.
Ошибок не обнаружено.
```

Foundation for a personal AI agent platform.

## Stack

- Python 3.13
- FastAPI
- aiogram 3
- httpx
- pydantic-settings
- SQLAlchemy 2
- Alembic
- PostgreSQL
- Loguru
- pytest
- Ruff
- mypy

## Setup

```bash
uv sync --dev
cp .env.example .env
docker compose up -d postgres
uv run uvicorn app.main:app --reload
```

If `uv` is unavailable:

```bash
python -m venv .venv
pip install -e ".[dev]"
```

## Interfaces

Run local CLI:

```bash
python -m app.cli
```

Run Telegram bot:

```bash
python -m app.run_bot
```

Required runtime variables for LLM and Telegram usage:

- `OPENROUTER_API_KEY`
- `OPENROUTER_MODEL`
- `TELEGRAM_BOT_TOKEN`

## Structure

```text
app/
  api/
  config/
  core/
  domain/
  llm/
  memory/
  planner/
  providers/
  router/
  telegram/
  tools/
  workers/
docker/
tests/
```

## Current Pipeline

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

## Quality

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run pytest
```
