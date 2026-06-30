from fastapi import FastAPI

from app.config.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    return FastAPI(debug=settings.debug, title=settings.name)


app = create_app()
