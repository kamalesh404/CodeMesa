# Getting Started

## Install

```bash
git clone https://github.com/kamalesh404/CodeMesa.git
cd CodeMesa
pip install -e ".[dev,ollama]"
```

For the local llama.cpp backend:
```bash
pip install -e ".[dev,local]"
```

## Choose a Backend

CodeMesa stays **free and unlimited** by default using a local model.

### Option A — Ollama (recommended)

```bash
# Install Ollama from ollama.com, then pull the best coding model
ollama pull qwen2.5-coder:7b

export CODEMESA_BACKEND=ollama
export CODEMESA_MODEL=qwen2.5-coder:7b
```

### Option B — llama.cpp (local GGUF)

Download a GGUF of Qwen2.5-Coder and point CodeMesa at it:

```bash
export CODEMESA_BACKEND=llama_cpp
export CODEMESA_MODEL=/path/to/qwen2.5-coder-7b-instruct.Q4_K_M.gguf
```

For 4GB VRAM set `n_gpu_layers` low (e.g. 8–16) so the rest offloads to RAM.

### Option C — OpenAI API (cloud, paid)

```bash
export CODEMESA_BACKEND=openai
export CODEMESA_MODEL=deepseek-coder
export CODEMESA_API_KEY=your-key
```

## Your First Build

```bash
codemesa build "build a CRUD task manager with Flask and SQLite"
```

Watch the agents work: the Architect designs it, the Planner orders the work,
the Coder writes each file, and the Reviewer checks it.

## Next Steps

- Read [architecture.md](architecture.md) to understand the pipeline.
- Read [agents.md](agents.md) for each agent's design.
- Read [models.md](models.md) for model recommendations by hardware.
