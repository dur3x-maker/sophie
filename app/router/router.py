from app.domain.commands import UserCommand
from app.router.base import BaseRouter
from app.workers.base import BaseWorker
from app.workers.registry import WORKER_REGISTRY


class RuleBasedRouter(BaseRouter):
    def route(self, command: UserCommand) -> type[BaseWorker]:
        text = command.text.lower()

        if any(keyword in text for keyword in ("docker", "compose", "container")):
            return WORKER_REGISTRY["devops"]
        if any(keyword in text for keyword in ("pytest", "test", "bug", "error", "баг")):
            return WORKER_REGISTRY["qa"]
        if any(keyword in text for keyword in ("post", "threads", "marketing", "пост")):
            return WORKER_REGISTRY["marketing"]
        return WORKER_REGISTRY["echo"]
