"""Tests for the parser."""

from src.core.parser import CodeParser, extract_python_code


def test_extract_python_code():
    text = 'Here you go:\n```python\nprint("hi")\n```'
    assert 'print("hi")' in extract_python_code(text)


def test_extract_files_with_path():
    text = '```python app.py\nprint(1)\n```'
    files = CodeParser.extract_files(text)
    assert files[0]["path"] == "app.py"
    assert files[0]["content"] == "print(1)"


def test_extract_files_uses_extension():
    text = '```python\nprint(1)\n```'
    files = CodeParser.extract_files(text)
    assert files[0]["path"] == "file.py"


def test_extract_multiple_blocks():
    text = '```python a.py\nx=1\n```\n```javascript b.js\ny=2\n```'
    files = CodeParser.extract_files(text)
    assert len(files) == 2
    assert files[1]["path"] == "b.js"
