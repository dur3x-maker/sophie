from typing import Any

import httpx

from app.core.exceptions import LLMProviderError
from app.core.logger import logger
from app.providers.base import BaseProvider


class OpenRouterProvider(BaseProvider):
    def __init__(self, api_key: str, model: str, base_url: str) -> None:
        self._api_key = api_key
        self._model = model
        self._base_url = base_url.rstrip("/")

    async def chat(self, messages: list[dict[str, str]]) -> str:
        if not self._api_key or not self._model:
            raise LLMProviderError("OpenRouter API key and model are required")

        request_url = f"{self._base_url}/chat/completions"

        try:
            async with httpx.AsyncClient(base_url=self._base_url, timeout=60.0) as client:
                response = await client.post(
                    "/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self._api_key}",
                        "Content-Type": "application/json",
                    },
                    json={"model": self._model, "messages": messages},
                )
                response.raise_for_status()
                return self._extract_text(response.json())
        except httpx.HTTPStatusError as exc:
            self._log_http_error(exc, request_url)
            raise LLMProviderError(
                "OpenRouter request failed "
                f"with status {exc.response.status_code}: {exc.response.text}"
            ) from exc
        except httpx.HTTPError as exc:
            self._log_http_error(exc, request_url)
            raise LLMProviderError("OpenRouter request failed") from exc
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMProviderError("OpenRouter response has unexpected format") from exc

    def _extract_text(self, payload: dict[str, Any]) -> str:
        content = payload["choices"][0]["message"]["content"]
        if not isinstance(content, str):
            raise ValueError("OpenRouter response content is not text")
        return content

    def _log_http_error(self, exc: httpx.HTTPError, request_url: str) -> None:
        response = getattr(exc, "response", None)
        request = getattr(exc, "request", None)
        url = str(request.url) if request is not None else request_url
        status = response.status_code if response is not None else "N/A"
        body = response.text if response is not None else "N/A"

        logger.error(
            "OpenRouter request failed\n\n"
            "URL:\n{url}\n\n"
            "Model:\n{model}\n\n"
            "Status:\n{status}\n\n"
            "Response:\n{body}\n\n"
            "Exception:\n{exception}",
            url=url,
            model=self._model,
            status=status,
            body=body,
            exception=repr(exc),
        )
