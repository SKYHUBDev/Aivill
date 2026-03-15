# AiVill API Documentation

<p align="center">
  <img src="../assets/aivill-logo.svg" width="150">
</p>

## Installation

```bash
pip install aivill
```

## Quick Start

```python
from aivill import VillainEngine

# Create and initialize engine
engine = VillainEngine()
engine.initialize({
    "data_dir": "data",
    "log_dir": "logs",
    "llm_model": "phi3.5"
})

# Set personality
engine.load_personality({
    "traits": {
        "aggression": 0.8,
        "patience": 0.4,
        "ego": 0.9,
        "chaos": 0.6,
        "adaptability": 0.7,
        "caution": 0.3
    }
})

# Update game state
game_state = {
    "player_health": 80,
    "villain_health": 100,
    "player_last_action": "attack",
    "round_number": 3
}
engine.update_state(game_state)

# Get villain decision
decision = engine.decide_action()
print(f"Villain action: {decision['action']}")

# Learn from result
result = {
    "outcome": "victory",
    "success": True,
    "reward": 1.0
}
engine.learn_from_result(result)

# Save memory
engine.save_memory()
```

## VillainEngine

The main class for the AiVill engine.

### Constructor

```python
VillainEngine(config: Optional[Dict[str, Any]] = None)
```

### Methods

#### initialize(config: Dict[str, Any]) -> None

Initialize the engine with configuration.

```python
engine.initialize({
    "name": "Lord of Shadows",
    "data_dir": "data",
    "log_dir": "logs",
    "llm_model": "phi3.5"
})
```

#### load_personality(profile: Dict[str, Any]) -> None

Load a personality profile.

```python
engine.load_personality({
    "traits": {
        "aggression": 0.8,
        "patience": 0.4,
        "ego": 0.9,
        "chaos": 0.6,
        "adaptability": 0.7,
        "caution": 0.3
    }
})
```

#### update_state(game_state: Dict[str, Any]) -> Dict[str, Any]

Update game state and get perceived observations.

```python
observations = engine.update_state({
    "player_health": 80,
    "villain_health": 100,
    "player_last_action": "attack",
    "round_number": 3,
    "available_actions": ["attack", "defend", "retreat"],
    "environment_objects": ["trap", "cover"]
})
```

#### decide_action() -> Dict[str, Any]

Make a decision based on current state.

Returns:
```python
{
    "action": "direct_attack",
    "strategy": "Intimidating",
    "strategy_id": "intimidating",
    "confidence": 0.75,
    "reasoning": "Player is aggressive"
}
```

#### learn_from_result(result: Dict[str, Any]) -> None

Learn from the outcome of a decision.

```python
engine.learn_from_result({
    "outcome": "victory",
    "success": True,
    "reward": 1.0,
    "damage_dealt": 20,
    "damage_received": 5
})
```

#### save_memory() -> None

Persist memory to disk.

#### load_memory() -> None

Load memory from disk.

#### get_player_profile(player_id: str) -> Optional[Dict[str, Any]]

Get learned player profile.

#### get_state_summary() -> Dict[str, Any]

Get engine state summary.

#### get_personality() -> Dict[str, float]

Get current personality traits.

#### get_llm_suggestion(prompt: str) -> Optional[str]

Get LLM-generated suggestion.

## Configuration

### Config Class

```python
from aivill import Config, default_config
```

#### Creating Config

```python
# From scratch
config = Config()

# From dictionary
config = Config({"name": "Custom Villain"})

# From file
config = Config.from_file("config.json")

# From environment
config = Config.from_env("AIVILL_")
```

#### Using Config

```python
# Get values
name = config.get("name")
aggression = config.get("personality.aggression")

# Set values
config.set("name", "New Villain")

# Get all as dict
config_dict = config.to_dict()
```

## Exceptions

All exceptions inherit from `AiVillError`:

```python
from aivill import (
    AiVillError,
    ConfigurationError,
    MemoryError,
    PersonalityError,
    StrategyError,
    LearningError,
    LLMError,
    OllamaNotAvailableError,
    DecisionError,
    PerceptionError,
    ValidationError,
)
```

## Game State Format

The game should provide state in this format:

```python
{
    "player_health": 80,           # Player health (0-100)
    "villain_health": 100,          # Villain health (0-100)
    "player_last_action": "attack", # Last player action
    "round_number": 3,             # Current round
    "available_actions": [         # Available villain actions
        "attack", "defend", "retreat", "set_trap", "taunt"
    ],
    "environment_objects": [        # Environment features
        "trap", "cover", "weapon", "treasure"
    ],
    "player_position": [4, 3],      # Optional: player position
    "player_id": "hero_001"        # Optional: player identifier
}
```

## Result Format

The game should provide results in this format:

```python
{
    "outcome": "victory",           # Outcome type
    "success": True,               # Was the action successful?
    "reward": 1.0,                 # Reward value (-1 to 1)
    "damage_dealt": 20,            # Damage dealt to player
    "damage_received": 5,          # Damage received from player
    "player_escaped": False,       # Did player escape?
    "trap_triggered": True         # Was a trap triggered?
}
```

## Personality Traits

| Trait | Range | Description |
|-------|-------|-------------|
| aggression | 0-1 | Preference for aggressive actions |
| patience | 0-1 | Willingness to wait and plan |
| ego | 0-1 | Risk tolerance and confidence |
| chaos | 0-1 | Tendency for random actions |
| adaptability | 0-1 | Speed of learning |
| caution | 0-1 | Defensive behavior |

## Examples

See `examples/` directory for more examples:

- `terminal_demo.py` - Interactive terminal demo
- `automated_test.py` - Automated test suite