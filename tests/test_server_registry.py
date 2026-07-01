import pytest

from app.config.settings import Settings
from app.devops.server_registry import ServerRegistry


def test_server_registry_returns_known_server_credentials() -> None:
    credentials = ServerRegistry(settings=_settings()).get("sweden")

    assert credentials.host == "sweden.example.com"
    assert credentials.username == "deploy"
    assert credentials.password == "secret"


def test_server_registry_rejects_unknown_server() -> None:
    with pytest.raises(KeyError, match="Unknown server"):
        ServerRegistry(settings=_settings()).get("germany")


def _settings() -> Settings:
    return Settings(
        server_sweden_host="sweden.example.com",
        server_sweden_username="deploy",
        server_sweden_password="secret",
    )
