from app.agent.loop import AgentLoop
from app.core.exceptions import LLMProviderError
from app.domain.commands import CommandResult, UserCommand
from app.llm.manager import LLMManager
from app.llm.prompt_builder import PromptBuilder
from app.memory.base import BaseMemory
from app.workers.base import BaseWorker

LLM_FALLBACK_MESSAGE = (
    "Я уже на связи, но LLM пока не подключена. "
    "Проверь OPENROUTER_API_KEY и OPENROUTER_MODEL в .env."
)


class LLMConversationWorker(BaseWorker):
    def __init__(
        self,
        llm_manager: LLMManager,
        memory: BaseMemory,
        prompt_builder: PromptBuilder,
        agent_loop: AgentLoop | None = None,
    ) -> None:
        self._llm_manager = llm_manager
        self._memory = memory
        self._prompt_builder = prompt_builder
        self._agent_loop = agent_loop or AgentLoop(llm_manager=llm_manager)

    async def handle(self, command: UserCommand) -> CommandResult:
        chat_id = str(command.metadata.get("chat_id") or command.user_id)
        history = await self._memory.history(chat_id)
        messages = self._prompt_builder.build(history=history, user_text=command.text)

        try:
            message = await self._agent_loop.run(messages)
        except LLMProviderError:
            return CommandResult(success=False, message=LLM_FALLBACK_MESSAGE)

        await self._memory.append(chat_id, "user", command.text)
        await self._memory.append(chat_id, "assistant", message)

        return CommandResult(success=True, message=message)
