"""Orchestrator — runs the full agent pipeline to build a project."""

from __future__ import annotations

import os
from typing import Any, Dict, List

from src.agents.architect import ArchitectAgent
from src.agents.coder import CoderAgent
from src.agents.planner import PlannerAgent
from src.agents.reviewer import ReviewerAgent
from src.core.llm import LLMInterface
from src.core.project import Project
from src.tools.file_writer import FileWriter
from src.tools.tree import build_tree


class Orchestrator:
    """Coordinates architect -> planner -> coder -> reviewer to build a project."""

    def __init__(self, llm: LLMInterface, output_dir: str) -> None:
        self.llm = llm
        self.output_dir = os.path.abspath(output_dir)
        self.project = Project(self.output_dir)
        self.architect = ArchitectAgent(llm)
        self.planner = PlannerAgent(llm)
        self.coder = CoderAgent(llm)
        self.reviewer = ReviewerAgent(llm)
        self.writer = FileWriter(self.output_dir)

    def build_from_scratch(self, user_request: str) -> Dict[str, Any]:
        """Run the entire pipeline starting from a raw request."""
        self.project.reset()

        design = self.architect.run(user_request)
        self.project.set_design(design)
        for f in design.get("files", []):
            self.project.register_file(f)

        plan = self.planner.run(design)
        self.project.set_plan(plan)

        for step in plan:
            file_path = step.get("file", "")
            context = self.project.describe()
            code = self.coder.run(step, context)
            review = self.reviewer.run(file_path, code, step.get("language", "text"))
            final_code = review.get("revised_code", code)
            if review.get("issues"):
                self.project.record_review(file_path, review["issues"])
            self.writer.write(file_path, final_code)
            self.project.mark_complete(step, review)

        self.project.set_tree(build_tree(self.output_dir))
        return self.project.summary()

    def continue_build(self) -> Dict[str, Any]:
        """Re-run remaining or add new steps to an existing build."""
        skipped = []
        for step in self.project.pending_steps():
            file_path = step.get("file", "")
            code = self.coder.run(step, self.project.describe())
            self.writer.write(file_path, code)
            self.project.mark_complete(step, {"passed": True, "issues": []})
        self.project.set_tree(build_tree(self.output_dir))
        return self.project.summary()
