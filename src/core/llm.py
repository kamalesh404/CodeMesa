"""LLM interface abstraction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class LLMInterface(ABC):
    """Minimal interface every backend implements."""

    name: str = "base"

    @abstractmethod
    def load(self, model_path: str | None = None, **kwargs: Any) -> None:
        """Load the model / configure the backend."""

    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        *,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> str:
        """Return the assistant's full reply text."""

    @abstractmethod
    def stream(
        self,
        messages: List[Dict[str, str]],
        *,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ):
        """Yield assistant reply tokens one by one."""

    @property
    @abstractmethod
    def loaded(self) -> bool:
        """Whether a model is loaded."""
