# AiVill Architecture

This document provides an in-depth look at AiVill's system architecture, module interactions, and data flows.

---

## System Overview

AiVill is built around a **central game loop** where the villain observes, decides, acts, and learns.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         GAME LOOP                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────┐    ┌──────────────┐    ┌────────────────────────┐     │
│  │  Game  │───▶│ Perception    │───▶│   Decision Engine     │     │
│  │ State  │    │   System      │    │                        │     │
│  └─────────┘    └──────────────┘    └────────────────────────┘     │
│       ▲                                        │                      │
│       │                                        ▼                      │
│       │            ┌──────────────────────────────┐                  │
│       │            │       Learning Engine        │                  │
│       │            │   (Pattern + Reinforcement) │                  │
│       │            └──────────────────────────────┘                  │
│       │                                        │                      │
│       │                                        ▼                      │
│       │            ┌──────────────────────────────┐                  │
│       │            │       Memory System          │                  │
│       │            │  (Profiles + Strategies)    │                  │
│       │            └──────────────────────────────┘                  │
│       │                                        │                      │
│       │                                        ▼                      │
│       │            ┌──────────────────────────────┐                  │
│       │            │    Personality Engine       │                  │
│       │            │  (Traits + Behavior Bias)   │                  │
│       │            └──────────────────────────────┘                  │
│       │                                                     │        │
│       └─────────────────────────────────────────────────────┘        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Core Modules

### 1. Perception System

**Location:** `aivill/core/perception.py`

Converts raw game state into structured observations.

**Input:**
```python
{
    "player_health": 70,
    "villain_health": 90,
    "player_last_action": "attack",
    "round_number": 5,
    "environment_objects": ["trap", "cover"]
}
```

**Output:**
```python
{
    "player_is_aggressive": True,
    "player_health_low": False,
    "villain_health_high": True,
    "environment_has_traps": True,
    "player_pattern_aggressive": True,
    "round_early": False,
    "round_late": False
}
```

**Responsibilities:**
- Health state analysis
- Player behavior pattern detection
- Environment feature extraction
- Round timing assessment

---

### 2. Memory System

**Location:** `aivill/memory/`

Manages persistent data across sessions.

#### Components

| Module | Purpose |
|--------|---------|
| `memory_manager.py` | Coordinates all memory systems |
| `player_profile.py` | Stores player behavior patterns |
| `strategy_memory.py` | Tracks strategy effectiveness |
| `short_term_memory.py` | Current game session data |

#### Data Flow

```
┌─────────────────────────────────────────┐
│           MEMORY SYSTEM                  │
├─────────────────────────────────────────┤
│                                          │
│  ┌─────────────────────────────────┐    │
│  │      PLAYER PROFILES            │    │
│  │  - action_frequency             │    │
│  │  - behavior_patterns            │    │
│  │  - games_played                │    │
│  │  - last_seen_strategies        │    │
│  └─────────────────────────────────┘    │
│                                          │
│  ┌─────────────────────────────────┐    │
│  │      STRATEGY MEMORY           │    │
│  │  - strategy_id                  │    │
│  │  - times_used                   │    │
│  │  - wins/losses                 │    │
│  │  - success_score                │    │
│  │  - mutation_origin             │    │
│  └─────────────────────────────────┘    │
│                                          │
│  ┌─────────────────────────────────┐    │
│  │    SHORT-TERM MEMORY           │    │
│  │  - recent_player_actions        │    │
│  │  - recent_villain_actions      │    │
│  │  - current_strategy            │    │
│  │  - round_number                 │    │
│  └─────────────────────────────────┘    │
│                                          │
└─────────────────────────────────────────┘
```

---

### 3. Personality Engine

**Location:** `aivill/personality/personality_engine.py`

Defines villain behavioral traits.

#### Traits

| Trait | Range | Effect |
|-------|-------|--------|
| `aggression` | 0-1 | Favors attack actions |
| `patience` | 0-1 | Delays actions, sets traps |
| `ego` | 0-1 | Prefers risky confrontations |
| `chaos` | 0-1 | Increases random moves |
| `adaptability` | 0-1 | Faster learning rate |
| `caution` | 0-1 | Defensive behavior |

#### Decision Formula

```
AdjustedScore = StrategyScore
               + (aggression * attack_weight)
               + (chaos * randomness_factor)
               - (caution * risk_factor)
```

#### Evolution

Personality adapts based on outcomes:
- **Victory** → Increases aggression, ego
- **Defeat** → Increases caution, patience
- **Pattern detected** → Increases adaptability

---

### 4. Strategy Engine

**Location:** `aivill/strategy/`

Manages tactical plans.

#### Strategy Structure

```python
{
    "strategy_id": "trap_corridor",
    "template": {
        "name": "Trap Corridor",
        "style": "tactical",
        "timing": "delayed",
        "focus": "defensive"
    },
    "effectiveness": 0.65,
    "use_count": 42,
    "success_count": 27,
    "failure_count": 15
}
```

#### Strategy Selection

1. Evaluate all strategies against current context
2. Apply personality modifiers
3. Consider player profile patterns
4. Add random noise for variety
5. Select highest scoring

---

### 5. Learning Engine

**Location:** `aivill/learning/`

Handles reinforcement learning.

#### Learning Pipeline

```
┌─────────────────────────────────────────────┐
│           LEARNING PIPELINE                 │
├─────────────────────────────────────────────┤
│                                              │
│  1. PATTERN RECOGNITION                      │
│     └─→ Analyze player action frequency     │
│     └─→ Detect aggressive/defensive patterns │
│     └─→ Predict next player action          │
│                                              │
│  2. REINFORCEMENT UPDATE                     │
│     └─→ Receive outcome (win/lose/draw)    │
│     └─→ Calculate reward (+1, 0, -1)        │
│     └─→ Update Q-score:                      │
│         Q_new = Q_old + α * (reward - Q_old)│
│                                              │
│  3. STRATEGY MUTATION                       │
│     └─→ Check if mutation needed             │
│     └─→ Apply mutation (add/remove/swap)    │
│     └─→ Initialize new strategy             │
│                                              │
└─────────────────────────────────────────────┘
```

#### Reward Calculation

```python
def calculate_reward(outcome, damage_dealt, damage_received):
    reward = 0.0
    
    if outcome == "victory":
        reward += 1.0
    elif outcome == "defeat":
        reward -= 1.0
    
    reward += damage_dealt * 0.02
    reward -= damage_received * 0.01
    
    return reward
```

---

### 6. Decision Engine

**Location:** `aivill/core/decision_engine.py`

Integrates all systems to produce final decision.

#### Decision Pipeline

```
predict_player_action()
        │
        ▼
evaluate_strategies()
        │
        ▼
apply_personality_bias()
        │
        ▼
consult_llm_if_needed()
        │
        ▼
select_best_action()
        │
        ▼
execute_action()
```

#### Output Format

```python
{
    "action": "direct_attack",
    "strategy": "Intimidating",
    "strategy_id": "intimidating",
    "confidence": 0.75,
    "reasoning": "Player is aggressive, ego is high"
}
```

---

### 7. LLM Interface

**Location:** `aivill/llm/ollama_client.py`

Optional Ollama integration.

#### Capabilities

* **Strategy Suggestions** — "What should I do against an aggressive player?"
* **Behavior Analysis** — "Analyze this player's patterns"
* **Dialogue Generation** — Villain taunts and monologue
* **Mutation Ideas** — Novel strategy variations

#### Models Tested

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| qwen2.5:1.5b | 986MB | Fast | Good |
| phi3.5 | 2.2GB | Medium | Better |
| llama3 | 4.9GB | Slow | Best |

---

### 8. Event Logger

**Location:** `aivill/logging/event_logger.py`

Records all interactions.

#### Log Format (JSONL)

```json
{"timestamp": "2024-01-15T10:30:00", "round": 5, "player_action": "attack", "villain_action": "defend", "strategy": "defensive_counter", "outcome": "neutral"}
{"timestamp": "2024-01-15T10:30:01", "round": 6, "player_action": "defend", "villain_action": "direct_attack", "strategy": "aggressive_rush", "outcome": "victory"}
```

#### Uses

* Debugging
* Analytics
* Training data
* Replay analysis

---

## Data Flow Summary

```
GAME ──▶ STATE ──▶ PERCEPTION ──▶ OBSERVATIONS
                                      │
                                      ▼
                                    MEMORY ──▶ PLAYER PROFILE
                                      │
                                      ▼
                              ┌───────┴───────┐
                              ▼               ▼
                       PERSONALITY       STRATEGY
                              │               │
                              └───────┬───────┘
                                      ▼
                              DECISION ENGINE
                                      │
                                      ▼
                              ACTION SELECTED
                                      │
                                      ▼
                              EXECUTE ACTION
                                      │
                                      ▼
                              LEARNING ENGINE
                                      │
                                      ▼
                              STRATEGY UPDATE
                                      │
                                      ▼
                                    MEMORY
```

---

## Configuration

See [Configuration Guide](configuration.md) for detailed config options.

---

## Extension Points

AiVill is designed for extension:

### Custom Components

1. **Perception** — Add new observation types
2. **Memory** — Different storage backends
3. **Learning** — New algorithms
4. **Strategy** — Custom tactics
5. **LLM** — Other providers

### Integration Points

```python
# Swap perception system
engine.perception = CustomPerception()

# Add custom memory
engine.memory = CustomMemory()

# Use different LLM
engine.ollama = CustomLLMClient()
```

---

## Performance

See [Performance Notes](performance.md) for optimization details.
