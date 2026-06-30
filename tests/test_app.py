from fastapi import FastAPI

from app.main import app


def test_app_is_fastapi_application() -> None:
    assert isinstance(app, FastAPI)
    assert app.title == "Sophie"
