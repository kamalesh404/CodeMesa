"""Tests for the syntax checker."""

from src.tools.syntax_check import validate


def test_valid_python():
    result = validate("def f():\n    return 1\n", "python")
    assert result["ok"] is True


def test_invalid_python():
    result = validate("def f(:\n", "python")
    assert result["ok"] is False
    assert result["errors"]


def test_valid_json():
    result = validate('{"a": 1}', "json")
    assert result["ok"] is True


def test_invalid_json():
    result = validate("{not json", "json")
    assert result["ok"] is False


def test_unknown_language_passes():
    result = validate("whatever", "ruby")
    assert result["ok"] is True
