import json
from typing import Any

from app.llm.manager import LLMManager
from app.tools.call import ToolCall
from app.tools.echo import EchoTool
from app.tools.manager import ToolManager
from app.tools.registry import ToolRegistry
from app.tools.result import ToolResult

MAX_AGENT_ITERATIONS = 5
AGENT_LOOP_LIMIT_MESSAGE = "Agent loop stopped after reaching iteration limit."


class AgentLoop:
    def __init__(
        self,
        llm_manager: LLMManager,
        tool_manager: ToolManager | None = None,
        max_iterations: int = MAX_AGENT_ITERATIONS,
    ) -> None:
        self._llm_manager = llm_manager
        self._tool_manager = tool_manager or ToolManager(
            registry=ToolRegistry(tools=[EchoTool]),
        )
        self._max_iterations = max_iterations

    async def run(self, messages: list[dict[str, str]]) -> str:
        loop_messages = list(messages)

        for _ in range(self._max_iterations):
            response = await self._llm_manager.chat(loop_messages)
            tool_call = self._parse_tool_call(response)
            if tool_call is None:
                return response

            loop_messages.append({"role": "assistant", "content": response})
            tool_result = await self._tool_manager.execute(
                tool_call.tool_name,
                **tool_call.arguments,
            )
            loop_messages.append(
                {
                    "role": "user",
                    "content": self._format_tool_result(tool_result),
                }
            )

        return AGENT_LOOP_LIMIT_MESSAGE

    def _parse_tool_call(self, response: str) -> ToolCall | None:
        try:
            payload = json.loads(response)
        except json.JSONDecodeError:
            return None

        if not isinstance(payload, dict):
            return None

        tool_name = payload.get("tool")
        arguments = payload.get("arguments", {})
        if not isinstance(tool_name, str) or not isinstance(arguments, dict):
            return None

        return ToolCall(tool_name=tool_name, arguments=dict(arguments))

    def _format_tool_result(self, tool_result: ToolResult) -> str:
        payload: dict[str, Any] = {
            "tool_result": tool_result.model_dump(mode="json"),
        }
        return json.dumps(payload, ensure_ascii=False)
