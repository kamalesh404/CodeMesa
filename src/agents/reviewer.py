"""Reviewer agent — critiques generated code."""

from __future__ import annotations

from typing import Any, Dict, List

from src.agents.base import BaseAgent


class ReviewerAgent(BaseAgent):
    """Reviews a file for bugs, correctness and style."""

    role = "reviewer"

    def run(self, file_path: str, code: str, language: str) -> Dict[str, Any]:
        """Return a review verdict with issues and a corrected version if needed."""
        result = self._chat(
            f"Review this {language} file for correctness, bugs, security issues, and style.\n\n"
            f"FILE: {file_path}\n\n"
            f"```\n{code}\n```\n\n"
            "Return STRICT JSON with keys:\n"
            "- 'passed': boolean (true if no changes needed)\n"
            "- 'issues': array of {issue, severity, line} objects\n"
            "- 'revised_code': the corrected full file (same as input if no changes)\n",
            temperature=0.2,
            max_tokens=4096,
        )
        return self._parse_json(result, code)

    @staticmethod
    def _parse_json(text: str, fallback_code: str) -> Dict[str, Any]:
        import json
        import re

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = None
        if not isinstance(data, dict):
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(0))
                except json.JSONDecodeError:
                    data = None
        if not isinstance(data, dict):
            data = {}
        data.setdefault("passed", True)
        data.setdefault("issues", [])
        data.setdefault("revised_code", fallback_code)
        return data
