"""llama.cpp backend — free, unlimited, local inference.

Optimized defaults for 4GB VRAM GPUs (e.g. GTX 2050).
"""

from __future__ import annotations

from typing import Any, Dict, List

from src.llms.base import LLMBackend


class LlamaCppBackend(LLMBackend):
    """Wraps llama-cpp-python for local GGUF models.

    ``n_gpu_layers`` controls how many layers run on the GPU. For a 4GB
    card use a modest value (e.g. 8-16) so the KV cache & activations
    stay within VRAM and the rest offloads to CPU/RAM.
    """

    name = "llama_cpp"

    def __init__(self, model_path: str | None = None, **kwargs: Any) -> None:
        super().__init__(model_path, **kwargs)
        self._llm = None

    def load(self, model_path: str | None = None, **kwargs: Any) -> None:
        from llama_cpp import Llama

        model_path = model_path or self.model_path
        if not model_path:
            raise ValueError("model_path is required for llama_cpp backend")
        opts = {
            "model_path": model_path,
            "n_ctx": self.options.get("n_ctx", 8192),
            "n_gpu_layers": kwargs.get("n_gpu_layers", self.options.get("n_gpu_layers", 0)),
            "n_threads": self.options.get("n_threads", 8),
            "verbose": False,
        }
        self._llm = Llama(**opts)
        self.model_path = model_path
        self._loaded = True

    def _complete(self, messages, temperature, max_tokens) -> str:
        if not self._llm:
            raise RuntimeError("Model not loaded. Call load() first.")
        prompt = self.format_prompt(messages)
        response = self._llm.create_completion(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=["<|im_end|>", "<|im_start|>"],
        )
        return response["choices"][0]["text"].strip()

    def chat(self, messages, *, temperature=0.3, max_tokens=2048) -> str:
        return self._complete(messages, temperature, max_tokens)

    def stream(self, messages, *, temperature=0.3, max_tokens=2048):
        if not self._llm:
            raise RuntimeError("Model not loaded. Call load() first.")
        prompt = self.format_prompt(messages)
        for part in self._llm.create_completion(
            prompt=prompt, temperature=temperature, max_tokens=max_tokens,
            stop=["<|im_end|>", "<|im_start|>"], stream=True,
        ):
            token = part["choices"][0]["text"]
            if token:
                yield token
