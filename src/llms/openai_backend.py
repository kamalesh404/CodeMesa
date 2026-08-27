"""OpenAI-compatible backend — optional cloud (DeepSeek, Together, etc.)."""

from __future__ import annotations

from typing import Any, Dict, List

from src.llms.base import LLMBackend


class OpenAIBackend(LLMBackend):
    """Uses an OpenAI-compatible HTTP API (e.g. DeepSeek-Coder, Together)."""

    name = "openai"

    def __init__(
        self,
        model: str = "deepseek-coder",
        base_url: str = "https://api.deepseek.com/v1",
        api_key: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(model, **kwargs)
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or self.options.get("api_key", "")

    def load(self, model_path: str | None = None, **kwargs: Any) -> None:
        if model_path:
            self.model = model_path
        if not self.api_key:
            raise ValueError("api_key is required for the OpenAI backend")
        self._loaded = True

    def _request(self, messages, temperature, max_tokens, stream=False) -> Any:
        import http.client
        import json

        parsed = self.base_url.replace("https://", "").replace("http://", "")
        secure = "https" in self.base_url
        payload = {
            "model": self.model, "messages": messages,
            "temperature": temperature, "max_tokens": max_tokens, "stream": stream,
        }
        body = json.dumps(payload).encode()
        if secure:
            conn = http.client.HTTPSConnection(parsed)
        else:
            conn = http.client.HTTPConnection(parsed)
        conn.request("POST", "/v1/chat/completions", body, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        })
        return conn

    def chat(self, messages, *, temperature=0.3, max_tokens=2048) -> str:
        conn = self._request(messages, temperature, max_tokens)
        resp = conn.getresponse()
        data = json.loads(resp.read().decode())
        conn.close()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError):
            return str(data)

    def stream(self, messages, *, temperature=0.3, max_tokens=2048):
        conn = self._request(messages, temperature, max_tokens, stream=True)
        resp = conn.getresponse()
        for raw in resp:
            line = raw.decode()
            if line.startswith("data:") and not line.startswith("data: [DONE]"):
                chunk = line[5:].strip()
                if chunk:
                    import json
                    try:
                        delta = json.loads(chunk)["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield delta
                    except (KeyError, IndexError, json.JSONDecodeError):
                        continue
        conn.close()
