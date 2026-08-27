"""Session-wide state shared across CLI invocations."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List


class SessionState:
    """Persists current project pointer and conversation context to disk."""

    def __init__(self, workdir: str = ".codemesa") -> None:
        self.workdir = workdir
        self.path = os.path.join(workdir, "session.json")
        self.data: Dict[str, Any] = {"project": None, "history": []}

    def load(self) -> None:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as fh:
                self.data = json.load(fh)

    def save(self) -> None:
        os.makedirs(self.workdir, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(self.data, fh, indent=2)

    def set_project(self, path: str) -> None:
        self.data["project"] = path
        self.save()

    def get_project(self) -> str | None:
        return self.data.get("project")

    def push_history(self, role: str, content: str) -> None:
        self.data["history"].append({"role": role, "content": content})
        self.data["history"] = self.data["history"][-50:]
        self.save()

    def history(self) -> List[Dict[str, str]]:
        return self.data.get("history", [])
