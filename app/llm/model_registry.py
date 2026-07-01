from collections.abc import Mapping

from app.config.models import DEFAULT_MODEL, WORKER_MODELS


class ModelRegistry:
    def __init__(
        self,
        worker_models: Mapping[str, str] | None = None,
        default_model: str = DEFAULT_MODEL,
    ) -> None:
        self._worker_models = dict(worker_models or WORKER_MODELS)
        self._default_model = default_model

    def get_model(self, worker_name: str) -> str:
        return self._worker_models.get(worker_name, self._default_model)
