import asyncio

from app.memory.in_memory import InMemoryConversationMemory, InMemoryMemory


def test_in_memory_conversation_memory_appends_messages() -> None:
    memory = InMemoryConversationMemory()

    asyncio.run(memory.append("chat-1", "user", "hello"))

    assert asyncio.run(memory.history("chat-1")) == [{"role": "user", "content": "hello"}]


def test_in_memory_conversation_memory_returns_chat_history() -> None:
    memory = InMemoryConversationMemory()

    asyncio.run(memory.append("chat-1", "user", "hello"))
    asyncio.run(memory.append("chat-1", "assistant", "hi"))
    asyncio.run(memory.append("chat-2", "user", "other"))

    assert asyncio.run(memory.history("chat-1")) == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi"},
    ]


def test_in_memory_conversation_memory_clears_chat_history() -> None:
    memory = InMemoryConversationMemory()

    asyncio.run(memory.append("chat-1", "user", "hello"))
    asyncio.run(memory.clear("chat-1"))

    assert asyncio.run(memory.history("chat-1")) == []


def test_in_memory_conversation_memory_keeps_last_20_messages() -> None:
    memory = InMemoryConversationMemory()

    for index in range(25):
        asyncio.run(memory.append("chat-1", "user", f"message-{index}"))

    history = asyncio.run(memory.history("chat-1"))

    assert len(history) == 20
    assert history[0] == {"role": "user", "content": "message-5"}
    assert history[-1] == {"role": "user", "content": "message-24"}


def test_in_memory_memory_alias_keeps_backward_compatibility() -> None:
    memory = InMemoryMemory()

    asyncio.run(memory.add_message("user-1", "user", "hello"))

    assert asyncio.run(memory.get_history("user-1")) == [{"role": "user", "content": "hello"}]
