from app.workers.base import BaseWorker
from app.workers.devops import DevOpsWorker
from app.workers.echo import EchoWorker
from app.workers.marketing import MarketingWorker
from app.workers.qa import QAWorker

WORKER_REGISTRY: dict[str, type[BaseWorker]] = {
    "devops": DevOpsWorker,
    "echo": EchoWorker,
    "marketing": MarketingWorker,
    "qa": QAWorker,
}
