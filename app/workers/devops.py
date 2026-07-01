from app.llm.manager import LLMManager
from app.llm.model_registry import ModelRegistry
from app.llm.prompt_builder import PromptBuilder
from app.memory.base import BaseMemory
from app.tools.base import BaseTool
from app.tools.registry import ToolRegistry
from app.workers.llm_conversation import LLMConversationWorker


class DevOpsWorker(LLMConversationWorker):
    name = "devops"
    prompt_path = "app/prompts/workers/devops.md"
    allowed_tool_names = (
        "ssh",
        "shell",
        "docker",
        "git",
        "filesystem",
        "http",
    )

    def __init__(
        self,
        llm_manager: LLMManager,
        memory: BaseMemory,
        prompt_builder: PromptBuilder,
        model_registry: ModelRegistry | None = None,
        tool_registry: ToolRegistry | None = None,
    ) -> None:
        super().__init__(
            llm_manager=llm_manager,
            memory=memory,
            prompt_builder=prompt_builder,
        )
        self.model = (model_registry or ModelRegistry()).get_model(self.name)
        self.allowed_tools: list[BaseTool] = (tool_registry or ToolRegistry()).get_many(
            self.allowed_tool_names
        )
