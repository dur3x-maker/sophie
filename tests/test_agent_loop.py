import asyncio
import json

from app.agent.loop import AGENT_LOOP_LIMIT_MESSAGE, AgentLoop
from app.llm.manager import LLMManager


class FakeLLMManager(LLMManager):
    def __init__(self, responses: list[str]) -> None:
        self._responses = responses
        self.messages: list[list[dict[str, str]]] = []

    async def chat(self, messages: list[dict[str, str]]) -> str:
        self.messages.append(messages)
        return self._responses.pop(0)


def test_agent_loop_returns_plain_text_response() -> None:
    llm_manager = FakeLLMManager(responses=["plain answer"])
    agent_loop = AgentLoop(llm_manager=llm_manager)

    result = asyncio.run(agent_loop.run([{"role": "user", "content": "hello"}]))

    assert result == "plain answer"
    assert len(llm_manager.messages) == 1


def test_agent_loop_executes_one_tool_and_returns_final_response() -> None:
    llm_manager = FakeLLMManager(
        responses=[
            '{"tool": "echo", "arguments": {"text": "hello"}}',
            "final answer",
        ]
    )
    agent_loop = AgentLoop(llm_manager=llm_manager)

    result = asyncio.run(agent_loop.run([{"role": "user", "content": "hello"}]))

    second_call = llm_manager.messages[1]
    tool_observation = json.loads(second_call[-1]["content"])

    assert result == "final answer"
    assert second_call[-2] == {
        "role": "assistant",
        "content": '{"tool": "echo", "arguments": {"text": "hello"}}',
    }
    assert tool_observation["tool_result"]["success"] is True
    assert tool_observation["tool_result"]["output"] == "echo"
    assert tool_observation["tool_result"]["metadata"] == {"tool_name": "echo"}


def test_agent_loop_executes_multiple_tools_before_final_response() -> None:
    llm_manager = FakeLLMManager(
        responses=[
            '{"tool": "echo", "arguments": {"text": "first"}}',
            '{"tool": "echo", "arguments": {"text": "second"}}',
            "final answer",
        ]
    )
    agent_loop = AgentLoop(llm_manager=llm_manager)

    result = asyncio.run(agent_loop.run([{"role": "user", "content": "hello"}]))

    third_call = llm_manager.messages[2]

    assert result == "final answer"
    assert len(llm_manager.messages) == 3
    assert json.loads(third_call[-1]["content"])["tool_result"]["output"] == "echo"
    assert third_call[-2]["content"] == '{"tool": "echo", "arguments": {"text": "second"}}'


def test_agent_loop_sends_unknown_tool_result_back_to_llm() -> None:
    llm_manager = FakeLLMManager(
        responses=[
            '{"tool": "unknown", "arguments": {}}',
            "unknown handled",
        ]
    )
    agent_loop = AgentLoop(llm_manager=llm_manager)

    result = asyncio.run(agent_loop.run([{"role": "user", "content": "hello"}]))

    tool_observation = json.loads(llm_manager.messages[1][-1]["content"])

    assert result == "unknown handled"
    assert tool_observation["tool_result"]["success"] is False
    assert tool_observation["tool_result"]["error"] == "Unknown tool: unknown"
    assert tool_observation["tool_result"]["metadata"] == {"tool_name": "unknown"}


def test_agent_loop_stops_after_iteration_limit() -> None:
    llm_manager = FakeLLMManager(responses=['{"tool": "echo", "arguments": {}}' for _ in range(5)])
    agent_loop = AgentLoop(llm_manager=llm_manager)

    result = asyncio.run(agent_loop.run([{"role": "user", "content": "hello"}]))

    assert result == AGENT_LOOP_LIMIT_MESSAGE
    assert len(llm_manager.messages) == 5
