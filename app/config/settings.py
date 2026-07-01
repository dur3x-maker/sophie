from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        extra="ignore",
        populate_by_name=True,
    )

    name: str = Field(default="Sophie")
    env: str = Field(default="local")
    debug: bool = Field(default=False)
    database_url: str = Field(
        default="postgresql+psycopg://sophie:sophie@localhost:5432/sophie",
        validation_alias=AliasChoices("DATABASE_URL", "APP_DATABASE_URL"),
    )
    openrouter_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("OPENROUTER_API_KEY", "APP_OPENROUTER_API_KEY"),
    )
    openrouter_model: str | None = Field(
        default=None,
        validation_alias=AliasChoices("OPENROUTER_MODEL", "APP_OPENROUTER_MODEL"),
    )
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        validation_alias=AliasChoices("OPENROUTER_BASE_URL", "APP_OPENROUTER_BASE_URL"),
    )
    telegram_bot_token: str | None = Field(
        default=None,
        validation_alias=AliasChoices("TELEGRAM_BOT_TOKEN", "APP_TELEGRAM_BOT_TOKEN"),
    )
    server_sweden_host: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SERVER_SWEDEN_HOST", "APP_SERVER_SWEDEN_HOST"),
    )
    server_sweden_username: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SERVER_SWEDEN_USERNAME", "APP_SERVER_SWEDEN_USERNAME"),
    )
    server_sweden_password: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SERVER_SWEDEN_PASSWORD", "APP_SERVER_SWEDEN_PASSWORD"),
    )
    server_france_host: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SERVER_FRANCE_HOST", "APP_SERVER_FRANCE_HOST"),
    )
    server_france_username: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SERVER_FRANCE_USERNAME", "APP_SERVER_FRANCE_USERNAME"),
    )
    server_france_password: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SERVER_FRANCE_PASSWORD", "APP_SERVER_FRANCE_PASSWORD"),
    )
    server_usa_host: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SERVER_USA_HOST", "APP_SERVER_USA_HOST"),
    )
    server_usa_username: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SERVER_USA_USERNAME", "APP_SERVER_USA_USERNAME"),
    )
    server_usa_password: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SERVER_USA_PASSWORD", "APP_SERVER_USA_PASSWORD"),
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
