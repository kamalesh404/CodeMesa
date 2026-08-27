"""Tests for agent behavior using the FakeLLM stub."""

from src.agents.architect import ArchitectAgent
from src.agents.coder import CoderAgent
from src.agents.planner import PlannerAgent
from src.agents.reviewer import ReviewerAgent
from tests.conftest import FakeLLM


def test_architect_parses_json():
    llm = FakeLLM(['{"name": "app", "language": "python", "files": ["main.py"]}'])
    agent = ArchitectAgent(llm)
    result = agent.run("build a web app")
    assert result["name"] == "app"
    assert "main.py" in result["files"]


def test_architect_falls_back_on_garbage():
    llm = FakeLLM(["not json at all"])
    agent = ArchitectAgent(llm)
    result = agent.run("build")
    assert result["name"] == "project"


def test_planner_parses_list():
    llm = FakeLLM(['[{"file": "main.py", "language": "python"}]'])
    agent = PlannerAgent(llm)
    steps = agent.run({"name": "x"})
    assert steps[0]["file"] == "main.py"


def test_coder_strips_fences():
    llm = FakeLLM(['```python\nprint(1)\n```'])
    agent = CoderAgent(llm)
    code = agent.run({"file": "main.py", "description": "x", "language": "python"}, "ctx")
    assert code.strip() == "print(1)"


def test_reviewer_returns_fallback():
    llm = FakeLLM(["garbage"])
    agent = ReviewerAgent(llm)
    review = agent.run("main.py", "print(1)", "python")
    assert review["passed"] is True
    assert review["revised_code"] == "print(1)"
