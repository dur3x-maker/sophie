from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.domain.commands import UserCommand
from app.router.router import RuleBasedRouter
from app.workers.base import BaseWorker
from app.workers.devops import DevOpsWorker
from app.workers.echo import EchoWorker
from app.workers.marketing import MarketingWorker
from app.workers.qa import QAWorker


@pytest.mark.parametrize(
    ("text", "expected_worker"),
    [
        ("проверь docker", DevOpsWorker),
        ("найди баг", QAWorker),
        ("напиши пост", MarketingWorker),
        ("привет", EchoWorker),
    ],
)
def test_rule_based_router_selects_worker(
    text: str,
    expected_worker: type[BaseWorker],
) -> None:
    command = UserCommand(
        id=uuid4(),
        text=text,
        source="test",
        user_id="user-1",
        created_at=datetime.now(UTC),
    )

    worker_cls = RuleBasedRouter().route(command)

    assert worker_cls is expected_worker


def test_rule_based_router_selects_devops_for_russian_docker_request() -> None:
    command = UserCommand(
        id=uuid4(),
        text="что с докером на швеции",
        source="test",
        user_id="user-1",
        created_at=datetime.now(UTC),
    )

    worker_cls = RuleBasedRouter().route(command)

    assert worker_cls is DevOpsWorker
