"""Abstract base for all agents."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.core.llm import LLMInterface
from src.core.prompts import AgentPrompts


class BaseAgent(ABC):
    """Base class for all CodeMesa agents.

    An agent wraps an LLM and a system prompt, and exposes a
    ``run`` method that turns an input into a structured output.
    """

    role: str = "agent"
    system_prompt: str = ""

    def __init__(self, llm: LLMInterface, context: Dict[str, Any] | None = None) -> None:
        self.llm = llm
        self.context: Dict[str, Any] = context or {}
        self.history: List[Dict[str, str]] = []
        self.prompts = AgentPrompts()

    def _system(self) -> str:
        return self.system_prompt or self.prompts.get(self.role)

    def _chat(self, user_input: str, *, temperature: float = 0.3, max_tokens: int = 2048) -> str:
        messages = [{"role": "system", "content": self._system()}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_input})
        self.history.append({"role": "user", "content": user_input})
        response = self.llm.chat(messages, temperature=temperature, max_tokens=max_tokens)
        self.history.append({"role": "assistant", "content": response})
        return response

    def reset(self) -> None:
        self.history.clear()

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the agent's primary task."""
