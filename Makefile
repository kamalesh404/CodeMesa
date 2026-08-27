.PHONY: install dev test lint check clean

install:
	pip install -e .

dev:
	pip install -e ".[dev,local,ollama]"

test:
	pytest

lint:
	ruff check src/ tests/

typecheck:
	mypy src/

check: lint typecheck test

build:
	codemesa build "create a task manager web app with Flask and SQLite"

clean:
	rm -rf build dist *.egg-info __pycache__ .pytest_cache generated
	find . -name "__pycache__" -type d -exec rm -rf {} +
