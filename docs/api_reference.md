# API Reference

## CLI

### `codemesa build "<request>"`

Build a complete project from scratch.

| Option | Description |
|--------|-------------|
| `--dir, -d <path>` | Output directory (default: `./generated`) |

### `codemesa continue-build`

Resume the last incomplete build (uses the active project).

### `codemesa status`

Print the current project's name, path, and file progress.

## Orchestrator

```python
from src.agents.orchestrator import Orchestrator
from src.llms import create_backend

llm = create_backend("ollama")
llm.load("qwen2.5-coder:7b")

orch = Orchestrator(llm, output_dir="./my-app")
summary = orch.build_from_scratch("build a URL shortener with FastAPI")
print(summary)  # {'name', 'root', 'files_planned', 'files_written', 'tree'}
```

## LLM Interface

```python
class LLMInterface(ABC):
    def load(self, model_path=None, **kwargs): ...
    def chat(self, messages, *, temperature=0.3, max_tokens=2048) -> str: ...
    def stream(self, messages, *, temperature=0.3, max_tokens=2048) -> Iterator[str]: ...
    @property
    def loaded(self) -> bool: ...
```

## Tools

```python
from src.tools.file_writer import FileWriter
from src.tools.tree import build_tree
from src.tools.syntax_check import validate

writer = FileWriter("./out")
writer.write("src/main.py", "print('hi')")

tree = build_tree("./out")
result = validate("def f(): pass", "python")
```
