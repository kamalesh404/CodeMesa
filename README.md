<div align="center">

# 🏗️ CodeMesa

**Multi-Agent AI Coding Assistant — Builds Complete Projects From Scratch**

[![License: MIT](https://img.shields.io/badge/License-MIT-448922?style=for-the-badge&logo=mit&logoColor=white)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![CLI](https://img.shields.io/badge/CLI-Click-000000?style=for-the-badge&logo=click&logoColor=white)](src/cli)
[![Multi-Agent](https://img.shields.io/badge/Architecture-Multi--Agent-FF6F00?style=for-the-badge&logo=minds&logoColor=white)]()
[![Local](https://img.shields.io/badge/FREE-Local%20LLM-00C853?style=for-the-badge&logo=llama&logoColor=white)](docs/models.md)

**Describe a project. CodeMesa designs it, plans it, writes every file, and reviews it.**

</div>

## What is CodeMesa?

CodeMesa is a **multi-agent AI coding assistant** that takes a plain-English request and produces a **complete, ready-to-develop project** — architecture, structure, every source file, tests, and documentation — automatically.

Unlike single-pass code generators, CodeMesa runs a **team of specialized agents** that think and collaborate before a single file is written.

## How It Works — The Agent Team

```
   You: "build a task manager web app with Flask and SQLite"
                        │
                        ▼
          ┌───────────────────────────┐
          │      ARCHITECT AGENT      │  Designs tech stack, file layout,
          │                           │  architecture decisions
          └────────────┬──────────────┘
                       │
                       ▼
          ┌───────────────────────────┐
          │      PLANNER AGENT        │  Breaks the build into ordered,
          │                           │  dependency-aware steps
          └────────────┬──────────────┘
                       │
          ┌────────────▼──────────────┐      ┌─────────────────────────┐
          │        CODER AGENT        │ ───▶ │      REVIEWER AGENT     │
          │  Writes one file per step │      │  Checks for bugs/style, │
          │                           │      │  revises if needed      │
          └────────────┬──────────────┘      └────────────┬────────────┘
                       │                                 │
                       └────────────┬────────────────────┘
                                    │
                                    ▼
          ┌───────────────────────────────┐
          │        ORCHESTRATOR          │  Coordinates the team,
          │  "intelligence" for the full  │  manages state & the project
          └───────────────────────────────┘
```

Each agent has a **specialized role** and its own system prompt (see `src/core/prompts.py`):

| Agent | Role |
|-------|------|
| **Architect** | Chooses stack, defines the file tree, records architecture decisions |
| **Planner** | Sequences steps so dependencies are built first |
| **Coder** | Writes complete, runnable code — one file per step |
| **Reviewer** | Finds bugs & style issues, returns a corrected version |
| **Orchestrator** | Runs the whole pipeline, tracks state, writes files safely |

## Quick Start

```bash
# Install
pip install -e .

# Point it at a local model backend (see docs/models.md)
export CODEMESA_BACKEND=ollama
export CODEMESA_MODEL=qwen2.5-coder:7b

# Build a complete project from scratch
codemesa build "build a REST API for a blog with FastAPI and SQLite"

# Build into a specific folder
codemesa build "a CLI markdown note app" --dir ./note-app

# Continue an incomplete build
codemesa continue-build

# Show project status
codemesa status
```

## Backends — Free & Unlimited

| Backend | Cost | Model | Setup |
|---------|------|-------|-------|
| **Ollama** ⭐ | Free, unlimited | `qwen2.5-coder:7b` | `pip install ".[ollama]"` + Ollama |
| **llama.cpp** | Free, unlimited | Local GGUF | `pip install ".[local]"` |
| **OpenAI API** | Paid | DeepSeek-Coder, etc. | `CODEMESA_API_KEY` |

For best **quality vs. cost** on a laptop, **`qwen2.5-coder:7b` via Ollama** is the sweet spot — it's a top coding model, fully local, free, and unlimited.

## Project Quality

- ✅ **Complete, runnable code** — no stubs, no TODOs, no placeholder comments
- ✅ **Dependency-aware planning** — infrastructure before the code that uses it
- ✅ **Automatic review pass** — the Reviewer agent re-checks every file
- ✅ **Safe writing** — prevents path traversal, creates dirs, tracks state
- ✅ **Syntax validation** — Python/JS/JSON verified before final write
- ✅ **Resumable builds** — interrupted builds can be continued

## Example

```bash
codemesa build "a URL shortener with Python, FastAPI and in-memory storage"
```

produces a folder like:

```
shortener/
├── src/
│   ├── __init__.py
│   ├── main.py            # FastAPI app
│   ├── models.py          # URL model
│   ├── store.py           # in-memory key-value store
│   └── routes.py          # /shorten, /{code} endpoints
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── requirements.txt
├── README.md
└── .gitignore
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `codemesa build "<request>"` | Build a complete project from scratch |
| `codemesa build "<request>" --dir <path>` | Build into a specific directory |
| `codemesa continue-build` | Resume the last incomplete build |
| `codemesa status` | Show the current project's state |

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CODEMESA_BACKEND` | `ollama` | Backend: `ollama`, `llama_cpp`, `openai` |
| `CODEMESA_MODEL` | `qwen2.5-coder:7b` | Model name |
| `CODEMESA_API_KEY` | — | API key for the OpenAI-compatible backend |

## License

MIT License — see [LICENSE](LICENSE)

<div align="center">
**Built with ❤️ by [Kamalesh](https://github.com/kamalesh404)**
</div>
