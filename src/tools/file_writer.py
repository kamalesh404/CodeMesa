"""Safe file writing with directory creation and overwrite protection."""

from __future__ import annotations

import os
from typing import Any


class FileWriter:
    """Writes files relative to a project root, creating directories as needed."""

    def __init__(self, root: str, *, overwrite: bool = True) -> None:
        self.root = os.path.abspath(root)
        self.overwrite = overwrite

    def write(self, rel_path: str, content: str) -> str:
        """Write content to ``rel_path`` under root. Returns absolute path."""
        # Prevent path traversal outside root
        abs_target = os.path.abspath(os.path.join(self.root, rel_path))
        if not abs_target.startswith(self.root + os.sep) and abs_target != self.root:
            raise ValueError(f"Refusing to write outside project root: {rel_path}")

        os.makedirs(os.path.dirname(abs_target) or self.root, exist_ok=True)
        if os.path.exists(abs_target) and not self.overwrite:
            raise FileExistsError(f"{rel_path} already exists")
        with open(abs_target, "w", encoding="utf-8") as fh:
            fh.write(content)
        return abs_target

    def write_batch(self, files: list[tuple[str, str]]) -> list[str]:
        written = []
        for rel_path, content in files:
            written.append(self.write(rel_path, content))
        return written
