from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        extra="ignore",
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


@lru_cache
def get_settings() -> Settings:
    return Settings()
