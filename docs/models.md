# Models

Choosing the right model is the most important decision for code quality.

## Recommended: `qwen2.5-coder:7b` (via Ollama)

For **best quality at zero cost**, `qwen2.5-coder:7b` is the pick:

- Top-tier among open 7B coding models (Qwen2.5-Coder family)
- Handles architecture, planning, and full-file generation well
- Runs locally on modest hardware via Ollama (no GPU required)
- **Free and unlimited**

```bash
ollama pull qwen2.5-coder:7b
export CODEMESA_BACKEND=ollama
export CODEMESA_MODEL=qwen2.5-coder:7b
```

## Model Tiers

| Tier | Model | Hardware | Best For |
|------|-------|----------|----------|
| Light | `qwen2.5-coder:1.5b` | Any laptop, CPU | Quick autocomplete, small scripts |
| Sweet spot ⭐ | `qwen2.5-coder:7b` | 8GB+ RAM / 4GB VRAM | Complete projects, this is the default |
| High quality | `qwen2.5-coder:14b` | 12GB+ RAM / 8GB VRAM | Larger projects, better reasoning |
| Top tier | `deepseek-coder` (API) | Cloud | Best possible code, paid tokens |
| Small+fast | `codellama:7b` | 4GB VRAM | Reliable, older but solid |

## 4GB VRAM (e.g. GTX 2050)

Choose `qwen2.5-coder:7b`. It uses CPU+GPU together so it runs fine. For a
fully-in-VRAM option use the Q3 quant of the 7B, or the 3B model for speed.

## OpenAI-Compatible (Paid, Cloud)

```bash
export CODEMESA_BACKEND=openai
export CODEMESA_MODEL=deepseek-coder
export CODEMESA_API_KEY=xxxx
```

Only switch to a paid API when you need the absolute best quality and have
budget/tokens to spend.
