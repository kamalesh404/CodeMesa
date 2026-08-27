"""Basic syntax validation of generated code."""

from __future__ import annotations

import ast
import shutil
import subprocess
import tempfile
from typing import Any, Dict, List


def validate(code: str, language: str) -> Dict[str, Any]:
    """Return {ok, errors} after a basic syntax check for supported languages."""
    lang = (language or "").lower()
    if lang in ("python", "py"):
        return _check_python(code)
    if lang in ("javascript", "js", "typescript", "ts"):
        return _check_node(code, ".ts" if lang in ("typescript", "ts") else ".js")
    if lang in ("json",):
        return _check_json(code)
    return {"ok": True, "errors": []}


def _check_python(code: str) -> Dict[str, Any]:
    try:
        ast.parse(code)
        return {"ok": True, "errors": []}
    except SyntaxError as e:
        return {"ok": False, "errors": [f"SyntaxError: {e.msg} (line {e.lineno})"]}


def _check_json(code: str) -> Dict[str, Any]:
    import json
    try:
        json.loads(code)
        return {"ok": True, "errors": []}
    except json.JSONDecodeError as e:
        return {"ok": False, "errors": [f"JSONDecodeError: {e.msg}"]}


def _check_node(code: str, ext: str) -> Dict[str, Any]:
    node = shutil.which("node")
    if not node:
        return {"ok": True, "errors": ["node not installed; skipping syntax check"]}
    with tempfile.NamedTemporaryFile("w", suffix=ext, delete=False, encoding="utf-8") as fh:
        fh.write(code)
        tmp = fh.name
    try:
        result = subprocess.run([node, "--check", tmp], capture_output=True, text=True)
        if result.returncode == 0:
            return {"ok": True, "errors": []}
        return {"ok": False, "errors": result.stderr.strip().splitlines()}
    finally:
        try:
            import os
            os.unlink(tmp)
        except OSError:
            pass
