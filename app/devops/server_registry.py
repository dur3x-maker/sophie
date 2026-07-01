from dataclasses import dataclass

from app.config.settings import Settings, get_settings


@dataclass(frozen=True)
class ServerCredentials:
    host: str
    username: str
    password: str


class ServerRegistry:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    def get(self, name: str) -> ServerCredentials:
        normalized_name = name.strip().lower()
        credentials = {
            "sweden": self._server(
                self._settings.server_sweden_host,
                self._settings.server_sweden_username,
                self._settings.server_sweden_password,
            ),
            "france": self._server(
                self._settings.server_france_host,
                self._settings.server_france_username,
                self._settings.server_france_password,
            ),
            "usa": self._server(
                self._settings.server_usa_host,
                self._settings.server_usa_username,
                self._settings.server_usa_password,
            ),
        }

        if normalized_name not in credentials:
            raise KeyError(f"Unknown server: {name}")

        server_credentials = credentials[normalized_name]
        if server_credentials is None:
            raise KeyError(f"Server is not configured: {name}")

        return server_credentials

    def _server(
        self,
        host: str | None,
        username: str | None,
        password: str | None,
    ) -> ServerCredentials | None:
        if not host or not username or not password:
            return None
        return ServerCredentials(host=host, username=username, password=password)
