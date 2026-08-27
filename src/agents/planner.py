"""Planner agent — breaks architecture into ordered steps."""

from __future__ import annotations

from typing import Any, Dict, List

from src.agents.base import BaseAgent


class PlannerAgent(BaseAgent):
    """Sequences the build into ordered, implementable steps."""

    role = "planner"

    def run(self, design: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Turn an architect design into an ordered list of build steps."""
        result = self._chat(
            f"Here is a project design:\n{design}\n\n"
            f"Break it into an ordered list of implementation steps. Each step must build "
            f"on the previous one (dependencies first).\n\n"
            f"Return STRICT JSON: an array of objects with keys:\n"
            f"- 'file': relative path to create/edit\n"
            f"- 'description': what this step implements\n"
            f"- 'depends_on': array of file paths this step depends on\n"
            f"- 'language': language of the file\n"
        )
        return self._parse_json(result)

    @staticmethod
    def _parse_json(text: str) -> List[Dict[str, Any]]:
        import json
        import re

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            pass
        else:
            if isinstance(data, list):
                return data
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
                if isinstance(data, list):
                    return data
            except json.JSONDecodeError:
                pass
        return [{
            "file": "main.py",
            "description": "Implement the core application",
            "depends_on": [],
            "language": "python",
        }]
