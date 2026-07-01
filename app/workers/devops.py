import json

from app.core.exceptions import LLMProviderError
from app.devops.server_registry import ServerCredentials, ServerRegistry
from app.domain.commands import CommandResult, UserCommand
from app.llm.manager import LLMManager
from app.llm.model_registry import ModelRegistry
from app.llm.prompt_builder import PromptBuilder
from app.memory.base import BaseMemory
from app.tools.base import BaseTool
from app.tools.manager import ToolManager
from app.tools.registry import ToolRegistry
from app.tools.result import ToolResult
from app.workers.llm_conversation import LLM_FALLBACK_MESSAGE, LLMConversationWorker

DOCKER_PS_COMMAND = "docker compose ps"
DOCKER_LOGS_COMMAND = "docker compose logs --tail=50"
DOCKER_DIAGNOSTIC_COMMANDS = (DOCKER_PS_COMMAND, DOCKER_LOGS_COMMAND)


class DevOpsWorker(LLMConversationWorker):
    name = "devops"
    prompt_path = "app/prompts/workers/devops.md"
    allowed_tool_names = ("ssh",)

    def __init__(
        self,
        llm_manager: LLMManager,
        memory: BaseMemory,
        prompt_builder: PromptBuilder,
        model_registry: ModelRegistry | None = None,
        tool_registry: ToolRegistry | None = None,
        tool_manager: ToolManager | None = None,
        server_registry: ServerRegistry | None = None,
    ) -> None:
        super().__init__(
            llm_manager=llm_manager,
            memory=memory,
            prompt_builder=prompt_builder,
        )
        self.model = (model_registry or ModelRegistry()).get_model(self.name)
        registry = tool_registry or ToolRegistry()
        self.allowed_tools: list[BaseTool] = registry.get_many(self.allowed_tool_names)
        self._tool_manager = tool_manager or ToolManager(registry=registry)
        self._server_registry = server_registry or ServerRegistry()

    async def handle(self, command: UserCommand) -> CommandResult:
        if not self._is_docker_status_request(command.text):
            return await super().handle(command)

        chat_id = str(command.metadata.get("chat_id") or command.user_id)
        history = await self._memory.history(chat_id)
        messages = self._prompt_builder.build(history=history, user_text=command.text)

        try:
            server_name = self._detect_server_name(command.text)
            server = self._server_registry.get(server_name)
            tool_results = await self._run_docker_diagnostics(server)
            messages.append(
                {
                    "role": "user",
                    "content": self._format_docker_observation(server_name, tool_results),
                }
            )
            message = await self._llm_manager.chat(messages)
        except LLMProviderError:
            return CommandResult(success=False, message=LLM_FALLBACK_MESSAGE)
        except (KeyError, ValueError) as exc:
            return CommandResult(success=False, message=str(exc))

        await self._memory.append(chat_id, "user", command.text)
        await self._memory.append(chat_id, "assistant", message)

        return CommandResult(success=True, message=message)

    def _is_docker_status_request(self, text: str) -> bool:
        normalized_text = text.casefold()
        return any(
            phrase in normalized_text
            for phrase in (
                "что с докером",
                "статус докера",
                "проверь докер",
                "docker status",
                "check docker",
            )
        )

    def _detect_server_name(self, text: str) -> str:
        normalized_text = text.casefold()
        if "швеци" in normalized_text or "sweden" in normalized_text:
            return "sweden"
        if "франци" in normalized_text or "france" in normalized_text:
            return "france"
        if "сша" in normalized_text or "usa" in normalized_text:
            return "usa"

        raise ValueError("Не понял, какой сервер проверить: Швеция, Франция или США.")

    async def _run_docker_diagnostics(self, server: ServerCredentials) -> list[ToolResult]:
        results: list[ToolResult] = []
        for diagnostic_command in DOCKER_DIAGNOSTIC_COMMANDS:
            results.append(
                await self._tool_manager.execute(
                    "ssh",
                    host=server.host,
                    username=server.username,
                    password=server.password,
                    command=diagnostic_command,
                    timeout=30.0,
                )
            )
        return results

    def _format_docker_observation(
        self,
        server_name: str,
        tool_results: list[ToolResult],
    ) -> str:
        payload = {
            "capability": "Remote Infrastructure",
            "server": server_name,
            "diagnostic": "docker compose",
            "results": [result.model_dump(mode="json") for result in tool_results],
            "instruction": "Сделай краткую человеческую выжимку состояния Docker.",
        }
        return json.dumps(payload, ensure_ascii=False)
