# Villain Personality Generator

Generate unique villain personalities for AiVill!

## Quick Start

```python
from villains import PersonalityGenerator, load_villain, list_villains

# Generate a random personality
generator = PersonalityGenerator()
villain = generator.generate_random()
print(villain)

# Generate from archetype
villain = generator.generate_from_archetype("the_mind_reader")

# Load a pre-made villain
villain = load_villain("chaos_overlord")
```

## Pre-made Villains

Load these villains directly:

| Name | Archetype | Key Traits |
|------|-----------|------------|
| trap_master | Cunning | High patience, adaptability |
| chaos_overlord | Chaotic | High aggression, chaos |
| mind_reader | Analytical | High patience, adaptability |
| berserker | Aggressive | High aggression, ego |
| turtle | Defensive | High caution, patience |
| trickster | Tricky | High chaos, adaptability |
| sadist | Cruel | High aggression, ego |
| mercenary | Practical | High adaptability |
| egomaniac | Arrogant | High ego, low patience |
| shadow | Stealthy | High patience, caution |

## Generating Villains

### Random Generation

```python
generator = PersonalityGenerator()

# Completely random
villain = generator.generate_random()

# Balanced (no extreme traits)
villain = generator.generate_balanced()

# Extreme (some traits very high/low)
villain = generator.generate_extreme()
```

### Archetype-based

```python
# From predefined archetypes
villain = generator.generate_from_archetype("the_calculating_tyrant")
villain = generator.generate_from_archetype("chaos_overlord")

# List available archetypes
print(generator.list_archetypes())
```

### With LLM Enhancement

```python
from aivill.llm import OllamaClient

llm = OllamaClient(model="qwen2.5")
generator = PersonalityGenerator(llm_client=llm)

villain = generator.generate_with_llm()
print(villain["description"])  # Now LLM-generated!
```

## Villain Profile Format

```python
villain = {
    "name": "The Calculating Tyrant",
    "traits": {
        "aggression": 0.65,
        "patience": 0.82,
        "ego": 0.70,
        "chaos": 0.21,
        "adaptability": 0.77,
        "caution": 0.45
    },
    "description": "A patient strategist who studies the player's weaknesses before striking."
}
```

## Use with VillainEngine

```python
from villains import load_villain
from aivill import VillainEngine

# Load pre-made villain
villain_data = load_villain("chaos_overlord")

# Create engine
engine = VillainEngine({"name": villain_data["name"]})

# Load personality
engine.load_personality({"traits": villain_data})
```

## Share Your Villains

Submit your custom villain profiles! Open a pull request to add new profiles to `profiles.py`.

## See Also

- [Experiment Playground](../experiments/README.md)
- [Villain Leaderboard](../leaderboard/README.md)
- [API Documentation](../docs/engine_api.md)
