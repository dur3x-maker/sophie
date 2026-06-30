from typing import Any

import httpx

from app.core.exceptions import LLMProviderError
from app.providers.base import BaseProvider


class OpenRouterProvider(BaseProvider):
    def __init__(self, api_key: str, model: str, base_url: str) -> None:
        self._api_key = api_key
        self._model = model
        self._base_url = base_url.rstrip("/")

    async def chat(self, messages: list[dict[str, str]]) -> str:
        try:
            async with httpx.AsyncClient(base_url=self._base_url, timeout=60.0) as client:
                response = await client.post(
                    "/chat/completions",
                    headers={"Authorization": f"Bearer {self._api_key}"},
                    json={"model": self._model, "messages": messages},
                )
                response.raise_for_status()
                return self._extract_text(response.json())
        except httpx.HTTPError as exc:
            raise LLMProviderError("OpenRouter request failed") from exc
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMProviderError("OpenRouter response has unexpected format") from exc

    def _extract_text(self, payload: dict[str, Any]) -> str:
        content = payload["choices"][0]["message"]["content"]
        if not isinstance(content, str):
            raise ValueError("OpenRouter response content is not text")
        return content
