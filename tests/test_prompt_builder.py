from app.llm.prompt_builder import PromptBuilder


def test_prompt_builder_builds_openrouter_messages() -> None:
    builder = PromptBuilder()
    history = [
        {"role": "user", "content": "first"},
        {"role": "assistant", "content": "answer"},
    ]

    messages = builder.build(history=history, user_text="second")

    assert messages[0]["role"] == "system"
    assert "Sophie" in messages[0]["content"]
    assert "инженерный ИИ-ассистент" in messages[0]["content"]
    assert messages[1:3] == history
    assert messages[-1] == {"role": "user", "content": "second"}
