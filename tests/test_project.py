"""Tests for project state management."""

import json

from src.core.project import Project


def test_project_reset(tmp_path):
    p = Project(str(tmp_path))
    p.set_design({"name": "x"})
    p.reset()
    assert p.design == {}


def test_project_register_and_complete(tmp_path):
    p = Project(str(tmp_path))
    p.register_file("app.py")
    assert not p.files["app.py"]
    p.mark_complete({"file": "app.py"}, {})
    assert p.files["app.py"]


def test_project_pending_steps(tmp_path):
    p = Project(str(tmp_path))
    plan = [
        {"file": "a.py", "description": "a"},
        {"file": "b.py", "description": "b"},
    ]
    p.set_plan(plan)
    p.mark_complete(plan[0], {})
    pending = p.pending_steps()
    assert len(pending) == 1
    assert pending[0]["file"] == "b.py"


def test_project_save_load(tmp_path):
    root = str(tmp_path)
    p = Project(root)
    p.set_design({"name": "hello"})
    p.set_plan([{"file": "a.py", "description": "a"}])
    p.save()
    loaded = Project.load(root)
    assert loaded.design["name"] == "hello"
    assert "a.py" in loaded.files


def test_project_summary(tmp_path):
    p = Project(str(tmp_path))
    p.set_design({"name": "demo"})
    p.set_plan([{"file": "a.py", "description": "a"}])
    s = p.summary()
    assert s["files_planned"] == 1
    assert s["files_written"] == 0
