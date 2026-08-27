"""Backend base class."""

from __future__ import annotations

from typing import Any, Dict, List

from src.core.llm import LLMInterface


class LLMBackend(LLMInterface):
    """Convenience base with shared helpers for text-formatting."""

    name = "backend"

    def __init__(self, model_path: str | None = None, **kwargs: Any) -> None:
        self.model_path = model_path
        self.options = kwargs
        self._loaded = False

    def load(self, model_path: str | None = None, **kwargs: Any) -> None:
        self.model_path = model_path or self.model_path
        self._loaded = True

    @property
    def loaded(self) -> bool:
        return self._loaded

    @staticmethod
    def format_prompt(messages: List[Dict[str, str]]) -> str:
        """Render a chat as plain text (generic fallback)."""
        parts = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role == "system":
                parts.append(f"<|im_start|>system\n{content}<|im_end|>")
            elif role == "assistant":
                parts.append(f"<|im_start|>assistant\n{content}<|im_end|>")
            else:
                parts.append(f"<|im_start|>user\n{content}<|im_end|>")
        parts.append("<|im_start|>assistant\n")
        return "\n".join(parts)
