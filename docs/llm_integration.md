# LLM Integration

AiVill can integrate with **Ollama** for local LLM-powered reasoning, dialogue generation, and strategy suggestions.

---

## Why Use LLMs?

LLMs add a layer of **intelligent reasoning** to the villain:

* **Strategy Suggestions** — "What should I do against an aggressive player?"
* **Behavior Analysis** — "What patterns is this player showing?"
* **Dialogue Generation** — Menacing taunts and monologue
* **Mutation Ideas** — Novel tactical variations

> **Note:** LLM calls add latency (~2-10 seconds). Consider disabling for real-time gameplay.

---

## Prerequisites

### 1. Install Ollama

Follow instructions at [ollama.ai](https://ollama.ai)

### 2. Pull a Model

```bash
# Smallest - Best for edge devices
ollama pull qwen2.5:1.5b    # 986MB

# Medium - Good balance
ollama pull phi3.5          # 2.2GB

# Large - Best quality
ollama pull llama3          # 4.9GB

# Alternative
ollama pull mistral        # 4.1GB
```

### 3. Verify Ollama is Running

```bash
ollama list
```

Should show your installed models.

---

## Model Comparison

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| qwen2.5:1.5b | 986MB | ~2s | Good | Edge deployment |
| phi3.5 | 2.2GB | ~5s | Better | Balanced use |
| llama3 | 4.9GB | ~10s | Best | Maximum quality |

---

## Quick Start

### Enable LLM

```python
from aivill import VillainEngine

# Using qwen2.5 (recommended for speed)
engine = VillainEngine({
    "llm_model": "qwen2.5",
    "llm_enabled": True
})

# Or phi3.5 for better quality
engine = VillainEngine({
    "llm_model": "phi3.5",
    "llm_enabled": True
})
```

### Check Connection

```python
print(f"LLM Available: {engine.llm_available}")
```

### Get Suggestions

```python
# Strategy suggestion
suggestion = engine.get_llm_suggestion(
    "The player keeps attacking aggressively. "
    "What strategy should the villain use?"
)
print(suggestion)

# Villain dialogue
taunt = engine.get_llm_suggestion(
    "Generate a menacing taunt from a villain "
    "who is winning against an aggressive player."
)
print(taunt)
```

---

## OllamaClient API

Direct access to the LLM client.

### Constructor

```python
from aivill.llm import OllamaClient

client = OllamaClient(
    base_url: str = "http://localhost:11434",
    model: str = "llama2"
)
```

### Methods

#### generate()

Generate text from prompt.

```python
response = client.generate(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 200
) -> Optional[str]
```

**Example:**

```python
response = client.generate(
    "What should a villain do when losing?",
    temperature=0.8
)
print(response)
```

#### generate_strategy_suggestion()

Get strategy advice.

```python
advice = client.generate_strategy_suggestion(
    strategy: Dict[str, Any],
    context: Dict[str, Any]
) -> Optional[str]
```

#### generate_taunt_or_dialogue()

Generate villain dialogue.

```python
taunt = client.generate_taunt_or_dialogue(
    context: Dict[str, Any],
    style: str = "menacing"
) -> Optional[str]
```

#### is_connected()

Check connection status.

```python
if client.is_connected():
    print("Ollama is ready!")
```

#### get_model_info()

Get current model info.

```python
info = client.get_model_info()
# {
#     "available": True,
#     "base_url": "http://localhost:11434",
#     "model": "qwen2.5"
# }
```

---

## Prompt Engineering

### Strategy Suggestion Prompt

```python
prompt = """
Player behavior summary:

attack_rate: {attack_rate}
defend_rate: {defend_rate}
trap_trigger_rate: {trap_trigger_rate}

Suggest a villain strategy to counter this player.
"""
```

### Behavior Analysis Prompt

```python
prompt = """
Analyze this player's behavior:

Recent actions: {recent_actions}
Win/loss record: {record}
Strategy used: {strategy}

What patterns do you notice?
"""
```

### Dialogue Generation Prompt

```python
prompt = """
Generate a {style} taunt for a villain in this situation:

Current health: {villain_health} vs {player_health}
Round: {round_number}
Recent outcome: {outcome}

Keep it short (1-2 sentences).
"""
```

---

## Best Practices

### 1. Use qwen2.5 for Production

```python
engine = VillainEngine({
    "llm_model": "qwen2.5"  # Fastest
})
```

### 2. Cache Responses

```python
# Don't call LLM every round
if round_number % 5 == 0:  # Every 5 rounds
    suggestion = engine.get_llm_suggestion(prompt)
```

### 3. Fallback Handling

```python
if engine.llm_available:
    suggestion = engine.get_llm_suggestion(prompt)
else:
    # Use deterministic decision
    suggestion = None
```

### 4. Temperature Control

```python
# For strategy: lower temperature = more consistent
client.generate(prompt, temperature=0.5)

# For dialogue: higher temperature = more creative
client.generate(prompt, temperature=0.9)
```

---

## Troubleshooting

### Ollama Not Running

```
Error: Ollama not available
```

**Solution:** Start Ollama:
```bash
ollama serve
```

### Model Not Found

```
Error: model not found
```

**Solution:** Pull the model:
```bash
ollama pull qwen2.5
```

### Slow Responses

**Solutions:**
1. Use smaller model (qwen2.5)
2. Reduce max_tokens
3. Increase temperature
4. Cache frequent prompts

### Connection Timeout

```python
# Increase timeout in OllamaClient
client = OllamaClient(timeout=60)
```

---

## Advanced Usage

### Custom System Prompt

```python
client = OllamaClient(
    model="qwen2.5",
    system_prompt="You are an evil mastermind in a fantasy game..."
)
```

### Stream Responses

```python
# For real-time dialogue
for response in client.generate_stream(prompt):
    print(response, end="", flush=True)
```

### Multiple Models

```python
# Use different models for different tasks
strategy_client = OllamaClient(model="qwen2.5")  # Fast
dialogue_client = OllamaClient(model="llama3")   # Creative
```

---

## Performance Notes

| Configuration | Response Time | Quality |
|--------------|---------------|---------|
| qwen2.5:1.5b | ~2s | Good |
| phi3.5 | ~5s | Better |
| llama3 | ~10s | Best |
| No LLM | <1ms | Deterministic |

---

## Future Enhancements

Planned LLM features:

* [ ] Vision integration (analyze game screens)
* [ ] Multi-modal reasoning
* [ ] Voice synthesis for dialogue
* [ ] Custom fine-tuned models
* [ ] Streaming responses
* [ ] Prompt caching
