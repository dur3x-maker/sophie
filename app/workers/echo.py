from app.workers.llm_conversation import (
    LLM_FALLBACK_MESSAGE,
    LLMConversationWorker,
)

__all__ = ["EchoWorker", "LLM_FALLBACK_MESSAGE"]


class EchoWorker(LLMConversationWorker):
    pass
