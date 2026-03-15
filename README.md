<p align="center">
<img src="https://raw.githubusercontent.com/instax-dutta/Aivill/main/assets/aivill-logo.png" width="220">
</p>

<h1 align="center">AiVill</h1>

<p align="center">
Adaptive AI Villains for Games
</p>

![PyPI](https://img.shields.io/pypi/v/aivill)
![Python](https://img.shields.io/pypi/pyversions/aivill)
![License](https://img.shields.io/pypi/l/aivill)
![Stars](https://img.shields.io/github/stars/instax-dutta/Aivill)

## Project Overview

AiVill is a modular AI engine designed to create adaptive villains that learn from player behavior and evolve strategies across gameplay sessions.

Most video game enemies are scripted AI that follow fixed logic. AiVill instead creates villains that observe, learn, adapt, and evolve — making each player encounter unique.

## Key Features

- **Adaptive Villain AI** — Villains that learn from player behavior and adapt strategies
- **Persistent Memory** — Remember player patterns across sessions
- **Reinforcement Learning** — Strategy effectiveness updates based on outcomes
- **Strategy Evolution** — Automatic mutation and improvement of tactics
- **Personality System** — Six trait dimensions that shape villain behavior
- **Ollama LLM Integration** — Optional local LLMs for reasoning and dialogue
- **Modular Architecture** — Swap components as needed
- **Game-Agnostic Design** — Integrate with any game genre
- **Simple API** — Full integration in under 10 lines of code

## Installation

```bash
pip install aivill
```

## Quick Example

```python
from aivill import VillainEngine

# Create and initialize
villain = VillainEngine()

# Game loop
while game_running:
    villain.update_state(game_state)
    action = villain.decide_action()
    villain.learn_from_result(result)

# Save memory for next session
villain.save_memory()
```

## How AiVill Works

The core functionality revolves around a continuous learning loop:

1. **Observe** — Game state updates the villain's perception
2. **Remember** — Player patterns stored in memory
3. **Decide** — Strategy selected based on personality + learning
4. **Act** — Villain executes action
5. **Learn** — Outcome updates strategy effectiveness
6. **Adapt** — Personality and strategies evolve

Over time, the villain becomes smarter and develops its own unique playstyle.

## Architecture

AiVill is built on a modular architecture:

```
Game
 ↓
AiVill Engine
 ├── Perception System (analyzes game state)
 ├── Memory System (stores player profiles)
 ├── Personality Engine (shapes decision-making)
 ├── Strategy Engine (manages tactics)
 ├── Learning Engine (reinforcement updates)
 ├── Decision Engine (action selection)
 ├── LLM Interface (optional reasoning)
 └── Event Logger (records interactions)
```

## Components

| Component | Description |
|----------|---------|
| **Perception System** | Analyzes game state, extracts observations |
| **Memory System** | Stores player profiles, strategy history, events |
| **Personality Engine** | Six trait dimensions affecting decision-making |
| **Strategy Engine** | Manages tactics, evaluates effectiveness |
| **Learning Engine** | Reinforcement updates, pattern recognition |
| **Decision Engine** | Integrates all systems to select actions |
| **LLM Interface** | Optional Ollama integration for reasoning |
| **Event Logger** | Records all interactions for analysis |

## Ollama Integration

AiVill can optionally use local LLMs via Ollama for enhanced reasoning.

### Setup

1. Install [Ollama](https://ollama.ai)
2. Pull a model:

```bash
ollama pull qwen2.5  # 986MB - Best for edge devices
ollama pull phi3.5   # 2.2GB - Good balance
ollama pull llama3   # 4.9GB - Most capable
```

### Enable LLM

```python
from aivill import VillainEngine

villain = VillainEngine({
    "llm_model": "qwen2.5",
    "llm_enabled": True
})
```

### LLM Features

- **Strategy Suggestions** — "What should the villain do against an aggressive player?"
- **Behavior Analysis** — "What patterns has this player shown?"
- **Villain Dialogue** — Generate menacing taunts and monologue
- **Strategy Mutation Ideas** — AI-generated tactical variations

> **Note:** LLM calls are slow (~2-10 seconds). Disable for real-time gameplay.

## Experiment Playground

The repository includes experiments to observe adaptive villain behavior:

```bash
# Learning demo - watch villain learn from player patterns
python experiments/learning_demo.py

# Strategy evolution demo - observe strategy mutations
python experiments/strategy_evolution_demo.py

# Pattern detection demo - test player pattern recognition
python experiments/player_pattern_test.py
```

What you'll see:
- **Learning Demo** — Villain win rate improves from ~20% to ~80% as it learns
- **Evolution Demo** — Strategies mutate and adapt over 100 rounds
- **Pattern Test** — Detect player archetypes (aggressive, defensive, evasive)

## Villain Personality Generator

Generate unique villain personalities:

```python
from villains import PersonalityGenerator

generator = PersonalityGenerator()

# Random personality
villain = generator.generate_random()

# From archetype
villain = generator.generate_from_archetype("the_mind_reader")

# Pre-made villains
from villains import load_villain
villain = load_villain("chaos_overlord")
```

Available archetypes:
- **the_calculating_tyrant** — Patient strategist
- **the_chaos_overlord** — Unpredictable force
- **the_mind_reader** — Master psychologist
- **the_aggressive_berserker** — Relentless warrior
- **the_defensive_turtle** — Impenetrable defense

## Configuration

### Personality Traits

| Trait | Range | Effect |
|-------|-------|--------|
| `aggression` | 0-1 | Prefers offensive actions |
| `patience` | 0-1 | Willing to wait and plan |
| `ego` | 0-1 | Risk tolerance, confidence |
| `chaos` | 0-1 | Tendency for random actions |
| `adaptability` | 0-1 | Speed of learning |
| `caution` | 0-1 | Defensive preference |

### Config File

```python
from aivill import Config

config = Config({
    "name": "Custom Villain",
    "llm_model": "qwen2.5",
    "personality": {
        "aggression": 0.7,
        "patience": 0.3,
        "ego": 0.8,
        "chaos": 0.2,
        "adaptability": 0.8,
        "caution": 0.2
    }
})
```

## Repository Structure

```
aivill/
├── aivill/                    # Main package
│   ├── __init__.py           # Exports
│   ├── config.py             # Configuration
│   ├── exceptions.py          # Custom exceptions
│   ├── core/                  # Engine, decisions
│   ├── memory/                # Memory management
│   ├── learning/              # Reinforcement learning
│   ├── strategy/              # Strategy engine + mutations
│   ├── personality/           # Personality traits
│   ├── llm/                   # Ollama client
│   └── logging/               # Event logger
│
├── examples/                  # Demo scripts
├── experiments/               # Research experiments
├── tests/                     # pytest suite
├── docs/                      # Documentation
└── pyproject.toml            # Package config
```

## Roadmap

- Advanced reinforcement learning algorithms
- Emergent strategy generation
- Multi-agent villain ecosystems
- Environment awareness system
- Visualization tools
- Unity/Unreal engine plugins
- Web-based dashboard

## Contributing

Contributions welcome! Areas of interest:
- AI Algorithms — Improve learning, strategy selection
- Strategy Mutations — Novel tactical variations
- Reinforcement Learning — Better reward functions
- LLM Prompts — More intelligent reasoning
- Game Integrations — Unity, Godot, Unreal wrappers
- Performance — Edge deployment optimizations

## License

MIT License — See [LICENSE](LICENSE) for details.

## Vision

AiVill aims to transform game villains from scripted obstacles into genuine adversaries that learn, adapt, and evolve. Every player deserves an antagonist who remembers their past victories, learns from their mistakes, develops a unique personality, and makes each encounter feel alive.

## Star History

If AiVill inspires you, please ⭐ star the repository to show your support!

[![Star History Chart](https://api.star-history.com/svg?repos=instax-dutta/Aivill&type=Date)](https://star-history.com/#instax-dutta/Aivill&Date)

**Star AiVill today and help create the next generation of game AI!**
