"""Build a text tree of a project directory."""

from __future__ import annotations

import os
from typing import List, Set

IGNORED = {
    ".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".venv", "venv", "env", "node_modules", ".codemesa", ".idea", ".vscode",
}


def build_tree(root: str, *, prefix: str = "", depth: int = -1) -> str:
    """Return an ASCII tree representation of ``root``."""
    root = os.path.abspath(root)
    lines: List[str] = [os.path.basename(root) or root]
    _walk(root, lines, "", depth, seen=set())
    return "\n".join(lines)


def _walk(directory: str, lines: List[str], prefix: str, depth: int, seen: Set[str]) -> None:
    if depth == 0:
        return
    try:
        entries = sorted(os.listdir(directory))
    except OSError:
        return
    entries = [e for e in entries if e not in IGNORED and not e.endswith(".pyc")]
    for i, name in enumerate(entries):
        path = os.path.join(directory, name)
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{name}")
        if os.path.isdir(path):
            real = os.path.realpath(path)
            if real in seen:
                continue
            seen.add(real)
            extension = "    " if is_last else "│   "
            _walk(path, lines, prefix + extension, depth - 1, seen)
