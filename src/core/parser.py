"""Extract code files from LLM responses."""

from __future__ import annotations

import re
from typing import Any, Dict, List


class CodeParser:
    """Parses LLM output into structured (path, language, content) files."""

    LANG_EXT = {
        "python": "py", "javascript": "js", "typescript": "ts",
        "html": "html", "css": "css", "json": "json",
        "yaml": "yml", "markdown": "md", "bash": "sh", "shell": "sh",
        "sql": "sql", "java": "java", "go": "go", "rust": "rs",
        "c": "c", "cpp": "cpp", "c++": "cpp", "ruby": "rb", "php": "php",
    }

    @staticmethod
    def extract_files(text: str) -> List[Dict[str, str]]:
        """Return list of {path, language, content} for each fenced block with a name."""
        files: List[Dict[str, str]] = []
        # Match ```lang (optionally with a path on the same line) ... ```
        pattern = re.compile(
            r"```(?P<lang>[a-zA-Z0-9_+.-]*)[ \t]*(?P<path>\S*)\s*\n(?P<content>.*?)```",
            re.DOTALL,
        )
        for m in pattern.finditer(text):
            lang = m.group("lang") or ""
            path = m.group("path")
            content = m.group("content")
            if not path:
                ext = CodeParser.LANG_EXT.get(lang.lower(), "txt")
                path = f"file.{ext}"
            content = content.rstrip("\n")
            files.append({"path": path, "language": lang, "content": content})
        return files


def extract_python_code(text: str) -> str:
    """Find the first ```python block and return it, else raw text."""
    blocks = CodeParser.extract_files(text)
    for b in blocks:
        if b["language"] == "python" or b["path"].endswith(".py"):
            return b["content"]
    return text.strip()
