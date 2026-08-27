"""Coder agent — writes a single file."""

from __future__ import annotations

from typing import Any, Dict

from src.agents.base import BaseAgent


class CoderAgent(BaseAgent):
    """Writes the code for one file based on the plan and project context."""

    role = "coder"

    def run(self, step: Dict[str, Any], project_context: str) -> str:
        """Generate code for a single file and return the raw file content."""
        result = self._chat(
            f"{project_context}\n\n"
            f"Now write the COMPLETE implementation for this file.\n"
            f"FILE PATH: {step.get('file')}\n"
            f"WHAT IT DOES: {step.get('description')}\n"
            f"LANGUAGE: {step.get('language')}\n\n"
            f"Rules:\n"
            f"- Output ONLY the file contents, no explanation, no markdown fences.\n"
            f"- Complete, runnable code. No stubs, no TODOs.\n"
            f"- Include imports, docstrings, and type hints.\n",
            temperature=0.2,
            max_tokens=4096,
        )
        return self._strip_fences(result)

    @staticmethod
    def _strip_fences(text: str) -> str:
        import re

        text = text.strip()
        # Remove ```lang ... ``` wrappers if present
        match = re.match(r"^```[a-zA-Z0-9_+-]*\s*\n?(.*?)\n?```$", text, re.DOTALL)
        if match:
            return match.group(1).rstrip() + "\n"
        return text
