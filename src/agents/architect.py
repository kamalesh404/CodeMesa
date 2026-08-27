"""Architect agent — designs the project."""

from __future__ import annotations

from typing import Any, Dict, List

from src.agents.base import BaseAgent


class ArchitectAgent(BaseAgent):
    """Designs the high-level structure of a new project.

    Produces:
      - recommended tech stack
      - directory / file layout
      - key architectural decisions
    """

    role = "architect"

    def run(self, user_request: str) -> Dict[str, Any]:
        """Analyze a free-form request and return a project design."""
        result = self._chat(
            f"Design a complete, production-grade project for the following request.\n\n"
            f"USER REQUEST:\n{user_request}\n\n"
            f"Return STRICT JSON with exactly these keys:\n"
            f"- 'name': project name (snake_case)\n"
            f"- 'description': one line\n"
            f"- 'language': main language\n"
            f"- 'stack': array of technologies/frameworks\n"
            f"- 'files': array of relative file paths to create\n"
            f"- 'decisions': array of architecture decisions\n"
        )
        return self._parse_json(result)

    @staticmethod
    def _parse_json(text: str) -> Dict[str, Any]:
        """Best-effort parse of JSON out of the raw response."""
        import json
        import re

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        return {
            "name": "project",
            "description": text.strip(),
            "language": "python",
            "stack": [],
            "files": [],
            "decisions": [],
        }
