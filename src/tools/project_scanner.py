"""Scan an existing project directory to build context for the agents."""

from __future__ import annotations

import os
from typing import Any, Dict, List

from src.tools.tree import IGNORED, build_tree


class ProjectScanner:
    """Collects file list + read-most recent state of an existing project."""

    MAX_READ_BYTES = 20_000

    def __init__(self, root: str) -> None:
        self.root = os.path.abspath(root)

    def list_files(self) -> List[str]:
        files: List[str] = []
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [d for d in dirnames if d not in IGNORED]
            for f in filenames:
                rel = os.path.relpath(os.path.join(dirpath, f), self.root)
                files.append(rel)
        return sorted(files)

    def build_context(self, *, include_tree: bool = True) -> Dict[str, Any]:
        files = self.list_files()
        sample: Dict[str, str] = {}
        for f in files:
            try:
                full = os.path.join(self.root, f)
                if os.path.getsize(full) <= self.MAX_READ_BYTES:
                    with open(full, "r", encoding="utf-8", errors="ignore") as fh:
                        sample[f] = fh.read()
            except OSError:
                continue
        return {
            "root": self.root,
            "files": files,
            "sample_sources": sample,
            "tree": build_tree(self.root) if include_tree else "",
        }

    def describe(self) -> str:
        ctx = self.build_context()
        lines = [f"EXISTING PROJECT AT: {ctx['root']}", "FILES:"]
        for f in ctx["files"][:200]:
            lines.append(f"  - {f}")
        if ctx.get("tree"):
            lines.append("TREE:")
            lines.append(ctx["tree"])
        return "\n".join(lines)
