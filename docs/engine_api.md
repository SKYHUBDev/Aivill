# AiVill Engine API

Complete API reference for the VillainEngine class.

---

## VillainEngine

The main class for the AiVill engine.

### Constructor

```python
VillainEngine(config: Optional[Dict[str, Any]] = None)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `config` | Dict | None | Initial configuration |

**Example:**

```python
from aivill import VillainEngine

engine = VillainEngine({
    "name": "Dark Lord",
    "data_dir": "data",
    "log_dir": "logs"
})
```

---

## Methods

### initialize()

Initialize the engine with configuration.

```python
initialize(config: Dict[str, Any]) -> None
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `config` | Dict | Configuration dictionary |

**Configuration Options:**

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `name` | str | "The Villain" | Villain name |
| `data_dir` | str | "data" | Memory storage directory |
| `log_dir` | str | "logs" | Event log directory |
| `llm_model` | str | None | Ollama model name |
| `llm_enabled` | bool | True | Enable LLM integration |
| `llm_temperature` | float | 0.7 | LLM generation temperature |
| `llm_max_tokens` | int | 200 | Max LLM response tokens |

**Example:**

```python
engine.initialize({
    "name": "Lord of Shadows",
    "data_dir": "data",
    "log_dir": "logs",
    "llm_model": "qwen2.5",
    "llm_enabled": True
})
```

---

### load_personality()

Load a personality profile.

```python
load_personality(profile: Dict[str, Any]) -> None
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `profile` | Dict | Personality profile |

**Profile Format:**

```python
engine.load_personality({
    "traits": {
        "aggression": 0.8,      # 0-1: Attack preference
        "patience": 0.4,         # 0-1: Planning vs spontaneity
        "ego": 0.9,             # 0-1: Risk tolerance
        "chaos": 0.3,           # 0-1: Random behavior
        "adaptability": 0.7,    # 0-1: Learning speed
        "caution": 0.3          # 0-1: Defensive tendency
    }
})
```

**Trait Effects:**

| Trait | High Value | Low Value |
|-------|-----------|-----------|
| aggression | Prefers attacks | Prefers defense |
| patience | Plans ahead | Acts impulsively |
| ego | Takes risks | Plays safely |
| chaos | Unpredictable | Consistent |
| adaptability | Learns fast | Slow learner |
| caution | Defensive | Aggressive |

---

### update_state()

Update game state and get perceived observations.

```python
update_state(game_state: Dict[str, Any]) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `game_state` | Dict | Current game state |

**Game State Format:**

```python
game_state = {
    # Required
    "player_health": 80,           # Player health (0-100)
    "villain_health": 100,         # Villain health (0-100)
    
    # Recommended
    "player_last_action": "attack", # Last action player took
    "round_number": 5,              # Current round number
    
    # Optional
    "available_actions": [          # What villain can do
        "attack", "defend", "retreat", 
        "set_trap", "taunt"
    ],
    "environment_objects": [        # What's in the environment
        "trap", "cover", "weapon", "treasure"
    ],
    "player_position": [4, 3],    # Player grid position
    "villain_position": [0, 0],    # Villain grid position
    "player_id": "hero_001"        # Player identifier
}
```

**Returns:**

```python
observations = {
    "player_is_aggressive": True,
    "player_health_low": False,
    "player_health_high": True,
    "villain_health_low": False,
    "environment_has_traps": True,
    "player_pattern_aggressive": True,
    "round_early": False,
    "round_mid": True,
    "round_late": False
}
```

**Example:**

```python
game_state = {
    "player_health": 70,
    "villain_health": 90,
    "player_last_action": "attack",
    "round_number": 5,
    "available_actions": ["attack", "defend", "taunt"],
    "environment_objects": ["trap", "cover"]
}

observations = engine.update_state(game_state)
```

---

### decide_action()

Make a decision based on current state.

```python
decide_action() -> Dict[str, Any]
```

**Returns:**

```python
decision = {
    "decision_id": 42,
    "action": "direct_attack",
    "strategy": "Intimidating",
    "strategy_id": "intimidating",
    "confidence": 0.75,
    "context": {
        "game_state": {...},
        "available_actions": [...],
        "player_id": "hero_001"
    },
    "timestamp": "2024-01-15T10:30:00.000000"
}
```

**Action Types:**

| Action | Description |
|--------|-------------|
| `direct_attack` | Aggressive offense |
| `scheming` | Planning and preparation |
| `opportunistic` | Exploiting weaknesses |
| `defensive` | Protecting self |
| `intimidating` | Psychological pressure |
| `negotiating` | Diplomatic approach |
| `chaotic` | Random unpredictable |

**Example:**

```python
decision = engine.decide_action()
print(f"Villain chooses: {decision['action']}")
print(f"Strategy: {decision['strategy']}")
print(f"Confidence: {decision['confidence']}")
```

---

### learn_from_result()

Learn from the outcome of a decision.

```python
learn_from_result(result: Dict[str, Any]) -> None
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `result` | Dict | Result of the action |

**Result Format:**

```python
result = {
    # Required
    "outcome": "victory",          # "victory", "defeat", "draw", "neutral"
    "success": True,               # Was the action successful?
    
    # Recommended
    "reward": 1.0,                # Explicit reward (-1 to 1)
    
    # Optional
    "damage_dealt": 20,            # Damage dealt to player
    "damage_received": 5,          # Damage received from player
    "player_escaped": False,       # Did player escape?
    "trap_triggered": True,        # Was a trap triggered?
    "trap_success": True            # Did trap work?
}
```

**Simple Format:**

```python
# Minimum required
engine.learn_from_result({
    "outcome": "victory",
    "success": True
})

# Or even simpler
engine.learn_from_result("victory")
```

**Example:**

```python
# Detailed result
engine.learn_from_result({
    "outcome": "victory",
    "success": True,
    "reward": 1.0,
    "damage_dealt": 25,
    "damage_received": 10,
    "trap_triggered": True
})

# Simple result
engine.learn_from_result({
    "outcome": "defeat",
    "success": False,
    "reward": -1.0
})
```

---

### save_memory()

Persist all memory to disk.

```python
save_memory() -> None
```

Saves:
- Player profiles
- Strategy memory
- Engine state (decisions, iterations)

**Example:**

```python
# After a game session
engine.save_memory()
print("Memory saved!")
```

---

### load_memory()

Load persisted memory from disk.

```python
load_memory() -> None
```

**Example:**

```python
# At start of new session
engine.load_memory()
print(f"Loaded {engine.total_decisions} previous decisions")
```

---

### get_player_profile()

Get learned profile for a player.

```python
get_player_profile(player_id: str) -> Optional[Dict[str, Any]]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `player_id` | str | Player identifier |

**Returns:**

```python
profile = {
    "player_id": "hero_001",
    "games_played": 5,
    "action_frequency": {
        "attack": 0.62,
        "defend": 0.18,
        "hide": 0.12,
        "explore": 0.08
    },
    "behavior_patterns": {
        "aggressive_start": True,
        "defensive_when_low_hp": True,
        "trap_avoidance_rate": 0.3
    },
    "trust_level": 0.2,
    "interaction_count": 42
}
```

**Example:**

```python
profile = engine.get_player_profile("hero_001")
if profile:
    print(f"Player attack rate: {profile['action_frequency']['attack']}")
```

---

### get_state_summary()

Get engine state summary.

```python
get_state_summary() -> Dict[str, Any]
```

**Returns:**

```python
summary = {
    "name": "Lord of Shadows",
    "total_decisions": 150,
    "total_learning_iterations": 142,
    "personality": {
        "aggression": 0.85,
        "patience": 0.55,
        "ego": 0.92,
        "chaos": 0.28,
        "adaptability": 0.75,
        "caution": 0.15
    },
    "strategy": {
        "current": "intimidating",
        "effectiveness": 0.68
    },
    "memory": {
        "player_profiles": 3,
        "total_strategies": 5,
        "total_uses": 150,
        "average_effectiveness": 0.65
    },
    "llm_available": True
}
```

**Example:**

```python
summary = engine.get_state_summary()
print(f"Villain: {summary['name']}")
print(f"Decisions: {summary['total_decisions']}")
print(f"Strategy: {summary['strategy']['current']}")
```

---

### get_personality()

Get current personality traits.

```python
get_personality() -> Dict[str, float]
```

**Returns:**

```python
traits = {
    "aggression": 0.8,
    "patience": 0.4,
    "ego": 0.9,
    "chaos": 0.3,
    "adaptability": 0.7,
    "caution": 0.3
}
```

**Example:**

```python
traits = engine.get_personality()
for trait, value in traits.items():
    bar = "#" * int(value * 10) + "-" * (10 - int(value * 10))
    print(f"{trait:12}: [{bar}] {value:.2f}")
```

---

### adapt_personality()

Manually adapt a personality trait.

```python
adapt_personality(trait: str, delta: float, reason: str = "") -> None
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `trait` | str | Trait name to modify |
| `delta` | float | Amount to change (-1 to 1) |
| `reason` | str | Optional reason for change |

**Example:**

```python
# Increase aggression after victories
engine.adapt_personality("aggression", 0.1, "Won several battles")

# Become more cautious after defeats
engine.adapt_personality("caution", 0.15, "Suffered losses")
```

---

### get_llm_suggestion()

Get LLM-generated suggestion.

```python
get_llm_suggestion(prompt: str) -> Optional[str]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | str | Question/prompt for LLM |

**Returns:**

```python
suggestion = "Against an aggressive player, consider using defensive traps..."
```

**Example:**

```python
if engine.llm_available:
    suggestion = engine.get_llm_suggestion(
        "What should the villain do against a very aggressive player?"
    )
    print(suggestion)
```

---

## Properties

### llm_available

Check if LLM is connected and available.

```python
@property
llm_available() -> bool
```

**Example:**

```python
if engine.llm_available:
    print("LLM is ready!")
else:
    print("LLM not available")
```

---

## Config Class

Configuration management.

### Creating Config

```python
from aivill import Config, default_config

# From scratch
config = Config()

# From dictionary
config = Config({"name": "Custom Villain"})

# From file
config = Config.from_file("config.json")

# From environment
config = Config.from_env("AIVILL_")
```

### Using Config

```python
# Get values (supports dot notation)
name = config.get("name")
aggression = config.get("personality.aggression")

# Set values
config.set("name", "New Villain")
config.set("personality.aggression", 0.9)

# Get all as dict
config_dict = config.to_dict()
```

---

## Exceptions

Custom exception types.

```python
from aivill import (
    AiVillError,              # Base exception
    ConfigurationError,       # Config issues
    MemoryError,              # Memory operations
    PersonalityError,         # Personality issues
    StrategyError,            # Strategy issues
    LearningError,            # Learning issues
    LLMError,                 # LLM operations
    OllamaNotAvailableError,  # Ollama not running
    DecisionError,            # Decision making
    PerceptionError,          # Perception issues
    ValidationError           # Input validation
)

try:
    engine.initialize(config)
except ConfigurationError as e:
    print(f"Config error: {e}")
```

---

## Full Example

```python
from aivill import VillainEngine

# Create engine
engine = VillainEngine({
    "name": "Lord of Shadows",
    "data_dir": "data",
    "log_dir": "logs",
    "llm_model": "qwen2.5"
})

# Set personality
engine.load_personality({
    "traits": {
        "aggression": 0.8,
        "patience": 0.4,
        "ego": 0.9,
        "chaos": 0.3,
        "adaptability": 0.7,
        "caution": 0.3
    }
})

# Load previous memory
engine.load_memory()

# Game loop
for round_num in range(1, 21):
    # Update state
    observations = engine.update_state({
        "player_health": 100 - (round_num * 5),
        "villain_health": 100 - (round_num * 3),
        "player_last_action": "attack",
        "round_number": round_num
    })
    
    # Get decision
    decision = engine.decide_action()
    
    # Execute in game...
    # outcome = game.execute(decision["action"])
    
    # Learn result
    engine.learn_from_result({
        "outcome": "victory" if round_num % 2 == 0 else "defeat",
        "success": round_num % 2 == 0,
        "damage_dealt": 20,
        "damage_received": 10
    })

# Save for next session
engine.save_memory()

# View stats
summary = engine.get_state_summary()
print(f"Completed {summary['total_decisions']} decisions")
```

---

## See Also

- [Architecture](architecture.md) - System design
- [Learning System](learning_system.md) - Learning algorithms
- [LLM Integration](llm_integration.md) - Ollama setup
