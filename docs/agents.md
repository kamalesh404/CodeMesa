# Agents

CodeMesa uses a team of specialized agents. Each has a distinct role, its own
system prompt (in `src/core/prompts.py`), and emits structured output consumed
by the next agent.

## Architect

**Input:** free-form user request.

**Output (JSON):**

```json
{
  "name": "taskmanager",
  "description": "A task manager web app",
  "language": "python",
  "stack": ["flask", "sqlite"],
  "files": ["app.py", "models.py", "templates/index.html", "requirements.txt"],
  "decisions": ["Use Flask with an in-memory SQLite DB"]
}
```

The Architect decides the *what*: tech stack, file layout, and architecture.

## Planner

**Input:** the Architect's design.

**Output (JSON array):**

```json
[
  {"file": "models.py", "description": "Define the Task model", "depends_on": [], "language": "python"},
  {"file": "app.py", "description": "Wire routes to the model", "depends_on": ["models.py"], "language": "python"}
]
```

The Planner decides the *order*: dependencies first, so each file compiles
against already-written code.

## Coder

**Input:** one plan step + project context.

**Output:** the complete file contents (fences stripped).

The Coder writes *one file at a time* with complete, runnable code — no stubs,
no TODOs, no explanations.

## Reviewer

**Input:** file path, generated code, language.

**Output (JSON):**

```json
{
  "passed": true,
  "issues": [{"issue": "unused import", "severity": "low", "line": 3}],
  "revised_code": "..."
}
```

The Reviewer catches bugs and style problems, and when needed returns a fully
corrected file.

## Orchestrator

The Orchestrator doesn't chat on its own — it **coordinates**:

1. Run Architect → design
2. Run Planner → plan
3. For each step: Coder → reviewer → write file → record state
4. Generate project tree & summary

It owns `Project` state and `FileWriter` safe-writing, and supports resuming
interrupted builds via `continue-build`.
