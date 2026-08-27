"""Backend factory."""

from __future__ import annotations

from src.core.llm import LLMInterface
from src.llms.llama_cpp_backend import LlamaCppBackend
from src.llms.ollama_backend import OllamaBackend
from src.llms.openai_backend import OpenAIBackend


def create_backend(provider: str, **kwargs) -> LLMInterface:
    """Instantiate a backend by name."""
    provider = provider.lower()
    if provider in ("llama_cpp", "llamacpp", "local", "gguf"):
        return LlamaCppBackend(**kwargs)
    if provider in ("ollama",):
        return OllamaBackend(**kwargs)
    if provider in ("openai", "deepseek", "openai_compatible"):
        return OpenAIBackend(**kwargs)
    raise ValueError(f"Unknown provider: {provider}")
