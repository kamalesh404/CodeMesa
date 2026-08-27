"""Ollama backend — optional local server."""

from __future__ import annotations

import json
import urllib.request
from typing import Any, Dict, List

from src.llms.base import LLMBackend


class OllamaBackend(LLMBackend):
    """Talks to a running Ollama server (default http://localhost:11434)."""

    name = "ollama"

    def __init__(self, model: str = "qwen2.5-coder:7b", base_url: str = "http://localhost:11434", **kwargs: Any) -> None:
        super().__init__(model, **kwargs)
        self.base_url = base_url.rstrip("/")
        self.model = model

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())

    def load(self, model_path: str | None = None, **kwargs: Any) -> None:
        if model_path:
            self.model = model_path
        self._loaded = True

    def chat(self, messages, *, temperature=0.3, max_tokens=2048) -> str:
        data = self._post("/api/chat", {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        })
        return data.get("message", {}).get("content", "").strip()

    def stream(self, messages, *, temperature=0.3, max_tokens=2048):
        payload = {
            "model": self.model, "messages": messages, "stream": True,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        req = urllib.request.Request(
            f"{self.base_url}/api/chat", data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req) as resp:
            for line in resp:
                chunk = json.loads(line)
                token = chunk.get("message", {}).get("content", "")
                if token:
                    yield token
