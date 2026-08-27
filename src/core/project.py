"""Project state model."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List


class Project:
    """Tracks design, plan, files and build status for a project."""

    def __init__(self, root: str) -> None:
        self.root = root
        self.design: Dict[str, Any] = {}
        self.plan: List[Dict[str, Any]] = []
        self.files: Dict[str, bool] = {}  # path -> generated?
        self.reviews: Dict[str, List[Any]] = {}
        self.tree: str = ""
        self.state_file = os.path.join(root, ".codemesa", "state.json")

    def reset(self) -> None:
        self.design = {}
        self.plan = []
        self.files = {}
        self.reviews = {}
        self.tree = ""

    def set_design(self, design: Dict[str, Any]) -> None:
        self.design = design

    def set_plan(self, plan: List[Dict[str, Any]]) -> None:
        self.plan = plan
        for step in plan:
            f = step.get("file")
            if f:
                self.files[f] = False

    def register_file(self, path: str) -> None:
        self.files[path] = False

    def mark_complete(self, step: Dict[str, Any], review: Dict[str, Any]) -> None:
        f = step.get("file")
        if f in self.files:
            self.files[f] = True

    def record_review(self, path: str, issues: List[Any]) -> None:
        self.reviews[path] = issues

    def set_tree(self, tree: str) -> None:
        self.tree = tree

    def pending_steps(self) -> List[Dict[str, Any]]:
        return [s for s in self.plan if not self.files.get(s.get("file", ""), True)]

    def describe(self) -> str:
        lines = ["PROJECT:", self.design.get("name", "project")]
        lines.append(f"DESCRIPTION: {self.design.get('description', '')}")
        lines.append("TECH STACK: " + ", ".join(self.design.get("stack", [])))
        lines.append("FILES TO CREATE:")
        for f in self.files:
            lines.append(f"  - {f}")
        if self.reviews:
            lines.append("KNOWN ISSUES:")
            for path, issues in self.reviews.items():
                lines.append(f"  - {path}: {len(issues)} issue(s)")
        return "\n".join(lines)

    def summary(self) -> Dict[str, Any]:
        return {
            "name": self.design.get("name", "project"),
            "root": self.root,
            "files_planned": len(self.files),
            "files_written": sum(1 for v in self.files.values() if v),
            "tree": self.tree,
        }

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        payload = {
            "design": self.design,
            "plan": self.plan,
            "files": self.files,
            "reviews": self.reviews,
            "tree": self.tree,
        }
        with open(self.state_file, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)

    @classmethod
    def load(cls, root: str) -> "Project":
        proj = cls(root)
        state_path = os.path.join(root, ".codemesa", "state.json")
        if os.path.exists(state_path):
            with open(state_path, "r", encoding="utf-8") as fh:
                payload = json.load(fh)
            proj.design = payload.get("design", {})
            proj.plan = payload.get("plan", [])
            proj.files = payload.get("files", {})
            proj.reviews = payload.get("reviews", {})
            proj.tree = payload.get("tree", "")
        return proj
