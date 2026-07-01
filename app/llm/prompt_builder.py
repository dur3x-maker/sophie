from importlib import resources


class PromptBuilder:
    def __init__(self, prompts_package: str = "app.prompts") -> None:
        self._system_prompt = self._load_prompt(prompts_package)

    def build(self, history: list[dict[str, str]], user_text: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": self._system_prompt},
            *history,
            {"role": "user", "content": user_text},
        ]

    def _load_prompt(self, prompts_package: str) -> str:
        prompt_parts = [
            resources.files(prompts_package).joinpath(file_name).read_text(encoding="utf-8").strip()
            for file_name in ("system.md", "personality.md", "behavior.md")
        ]
        return "\n\n".join(part for part in prompt_parts if part)
