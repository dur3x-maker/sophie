from app.config.models import DEFAULT_MODEL, WORKER_MODELS
from app.llm.model_registry import ModelRegistry


def test_model_registry_returns_worker_model() -> None:
    registry = ModelRegistry(worker_models={"devops": "custom/devops"})

    assert registry.get_model("devops") == "custom/devops"


def test_model_registry_returns_default_for_unknown_worker() -> None:
    registry = ModelRegistry(default_model="custom/default", worker_models={})

    assert registry.get_model("unknown") == "custom/default"


def test_worker_models_include_known_workers() -> None:
    assert WORKER_MODELS == {
        "devops": DEFAULT_MODEL,
        "marketing": DEFAULT_MODEL,
        "qa": DEFAULT_MODEL,
    }
