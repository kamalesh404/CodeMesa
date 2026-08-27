"""Shared fixtures."""

import pytest

from src.agents.architect import ArchitectAgent
from src.core.llm import LLMInterface


class FakeLLM(LLMInterface):
    """Deterministic stub LLM used to test agents without a real model."""

    name = "fake"
    responses = []

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []
        self._loaded = True

    def load(self, model_path=None, **kwargs):
        self._loaded = True

    def chat(self, messages, *, temperature=0.3, max_tokens=2048):
        self.calls.append(messages)
        return self.responses.pop(0) if self.responses else "{}"

    def stream(self, messages, *, temperature=0.3, max_tokens=2048):
        yield "ok"

    @property
    def loaded(self):
        return self._loaded


@pytest.fixture
def fake_llm():
    return FakeLLM(["{'name': 'x'}"])


@pytest.fixture
def fake_llm_noop():
    return FakeLLM([])
