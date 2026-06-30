import asyncio

from app.memory.in_memory import InMemoryMemory


def test_in_memory_memory_adds_messages() -> None:
    memory = InMemoryMemory()

    asyncio.run(memory.add_message("user-1", "user", "hello"))

    assert asyncio.run(memory.get_history("user-1")) == [{"role": "user", "content": "hello"}]


def test_in_memory_memory_returns_user_history() -> None:
    memory = InMemoryMemory()

    asyncio.run(memory.add_message("user-1", "user", "hello"))
    asyncio.run(memory.add_message("user-1", "assistant", "hi"))
    asyncio.run(memory.add_message("user-2", "user", "other"))

    assert asyncio.run(memory.get_history("user-1")) == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi"},
    ]


def test_in_memory_memory_clears_user_history() -> None:
    memory = InMemoryMemory()

    asyncio.run(memory.add_message("user-1", "user", "hello"))
    asyncio.run(memory.clear("user-1"))

    assert asyncio.run(memory.get_history("user-1")) == []


def test_in_memory_memory_keeps_last_20_messages() -> None:
    memory = InMemoryMemory()

    for index in range(25):
        asyncio.run(memory.add_message("user-1", "user", f"message-{index}"))

    history = asyncio.run(memory.get_history("user-1"))

    assert len(history) == 20
    assert history[0] == {"role": "user", "content": "message-5"}
    assert history[-1] == {"role": "user", "content": "message-24"}
