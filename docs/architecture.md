# Architecture

CodeMesa is built around a **pipeline of specialized agents** coordinated by an
orchestrator. This document explains each component.

## Execution Flow

```
build_from_scratch(request)
        │
        ▼
 ┌───────────────┐   JSON design
 │  Architect    │──────────────┐
 └───────────────┘              │
        │ design                ▼
        ▼              ┌───────────────┐
        │              │   Planner     │  ordered steps
        └─────────────▶│               │──────────────┐
                       └───────────────┘              │
                                                      ▼
              ┌───────────────────────────────────────────────┐
              │         loop over plan steps                  │
              │                                               │
              │   step ─▶ Coder ─▶ code ─▶ Reviewer ─▶ file   │
              │              │                 │              │
              │              └─── revised ─────┘              │
              │                                               │
              └───────────────────────────────────────────────┘
                                │
                                ▼
                       tree + summary
```

## Modules

### `src/agents/`
- **`base.py`** — `BaseAgent` with `run()` and shared chat/context handling.
- **`architect.py`** — outputs `{name, description, language, stack, files, decisions}`.
- **`planner.py`** — outputs `[{file, description, depends_on, language}]`.
- **`coder.py`** — writes one file; strips markdown fences.
- **`reviewer.py`** — returns `{passed, issues, revised_code}`.
- **`orchestrator.py`** — owns the pipeline, project state, and file writing.

### `src/core/`
- **`llm.py`** — `LLMInterface` ABC implemented by every backend.
- **`prompts.py`** — central prompt registry keyed by agent role.
- **`parser.py`** — extracts code blocks/paths from LLM output.
- **`project.py`** — `Project` model: design, plan, files, reviews, tree.
- **`state.py`** — `SessionState`: persists active project & history.

### `src/llms/`
- **`base.py`** — `LLMBackend` with a generic ChatML prompt formatter.
- **`llama_cpp_backend.py`** — local GGUF via llama-cpp-python (4GB-VRAM tuned).
- **`ollama_backend.py`** — local Ollama server (free & unlimited).
- **`openai_backend.py`** — any OpenAI-compatible API.

### `src/tools/`
- **`file_writer.py`** — safe writes, dir creation, path-traversal guard.
- **`tree.py`** — ASCII project tree generator.
- **`syntax_check.py`** — Python/JS/JSON validation.
- **`project_scanner.py`** — reads an existing project for context.

## Design Principles

1. **Deterministic orchestration, creative agents.** The pipeline logic is
   explicit and testable; only the agents are generative.
2. **JSON contracts between agents.** Each agent emits structured output that
   the next consumes, making the flow reliable and inspectable.
3. **State on disk.** A build can be resumed from `.codemesa/state.json`.
4. **Backend-agnostic.** Agents talk to `LLMInterface`, so the same pipeline
   runs free locally or on paid cloud APIs.
