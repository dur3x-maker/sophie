# Sophie

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

## Quality

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run pytest
```
