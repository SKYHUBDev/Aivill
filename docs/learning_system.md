# Learning System

AiVill uses a hybrid learning system combining **pattern recognition** and **reinforcement learning** to create adaptive villain behavior.

---

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  LEARNING PIPELINE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐    ┌─────────────────────────────┐   │
│  │      INPUT      │───▶│     PATTERN RECOGNITION      │   │
│  │                 │    │  • Player action frequency   │   │
│  │ • Game State    │    │  • Behavior sequences        │   │
│  │ • Player Action │    │  • Strategic patterns        │   │
│  │ • Outcome       │    └─────────────────────────────┘   │
│  │                 │                  │                      │
│  └─────────────────┘                  ▼                      │
│                         ┌─────────────────────────────┐     │
│                         │   REINFORCEMENT LEARNING   │     │
│                         │  • Q-score updates          │     │
│                         │  • Reward calculation       │     │
│                         │  • Strategy selection       │     │
│                         └─────────────────────────────┘     │
│                                       │                     │
│                                       ▼                     │
│                         ┌─────────────────────────────┐     │
│                         │   STRATEGY EVOLUTION        │     │
│                         │  • Mutation triggers         │     │
│                         │  • New strategies           │     │
│                         │  • Hybrid combinations       │     │
│                         └─────────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Pattern Recognition

**Location:** `aivill/learning/pattern_learning.py`

Analyzes player behavior to detect patterns.

### What It Tracks

```python
player_profile = {
    "action_frequency": {
        "attack": 0.62,      # 62% attack
        "defend": 0.18,      # 18% defend
        "explore": 0.12,     # 12% explore
        "hide": 0.08         # 8% hide
    },
    "behavior_patterns": {
        "aggressive_start": True,      # Opens aggressively
        "defensive_when_low_hp": True,  # Defensive at low health
        "trap_awareness": 0.3,          # Avoids traps 30%
        "predictable_patterns": 0.7     # High predictability
    }
}
```

### Pattern Detection

```python
def detect_patterns(player_history):
    # Calculate action frequencies
    frequencies = calculate_frequencies(player_history)
    
    # Detect sequences
    sequences = detect_sequences(player_history)
    
    # Identify tendencies
    tendencies = {
        "aggressive": frequencies["attack"] > 0.5,
        "defensive": frequencies["defend"] > 0.4,
        "explorer": frequencies["explore"] > 0.3,
        "cautious": frequencies["hide"] > 0.2
    }
    
    return {
        "frequencies": frequencies,
        "sequences": sequences,
        "tendencies": tendencies
    }
```

### Prediction

```python
def predict_player_action(player_profile):
    """Predict player's next action based on patterns."""
    
    # If player always attacks first
    if player_profile["aggressive_start"]:
        return "attack"
    
    # If player defends when low HP
    if player_profile["defensive_when_low_hp"] and player["low_health"]:
        return "defend"
    
    # Default to most frequent action
    return max(player_profile["action_frequency"].items())[0]
```

---

## Reinforcement Learning

**Location:** `aivill/learning/reinforcement.py`

Uses Q-learning to update strategy effectiveness.

### Q-Learning Basics

```
Q(s, a) = Q(s, a) + α * (r + γ * max Q(s', a') - Q(s, a))

Where:
- s = current state
- a = action taken
- r = reward received
- α = learning rate (0.1)
- γ = discount factor (0.9)
```

### Reward Calculation

```python
def calculate_reward(outcome, damage_dealt, damage_received):
    """
    Calculate reward from action outcome.
    
    Returns: float between -1 and 1
    """
    reward = 0.0
    
    # Outcome reward
    if outcome == "victory":
        reward += 1.0
    elif outcome == "defeat":
        reward -= 1.0
    elif outcome == "draw":
        reward += 0.0
    
    # Damage reward
    reward += damage_dealt * 0.02    # Positive for dealing damage
    reward -= damage_received * 0.01  # Negative for taking damage
    
    # Clamp to [-1, 1]
    return max(-1.0, min(1.0, reward))
```

### Strategy Score Update

```python
def update_strategy_score(strategy, reward):
    """Update strategy effectiveness score."""
    
    learning_rate = 0.1
    
    # New score = old score + learning rate * error
    old_score = strategy["effectiveness"]
    new_score = old_score + learning_rate * (reward - old_score)
    
    # Clamp to [0, 1]
    strategy["effectiveness"] = max(0.0, min(1.0, new_score))
    
    return new_score
```

---

## Strategy Evolution

**Location:** `aivill/strategy/mutation.py`

Strategies evolve through mutation to prevent stagnation.

### Mutation Triggers

| Trigger | Condition |
|---------|-----------|
| High Loss Rate | success_rate < 0.3 |
| Unused Strategy | 50+ rounds without use |
| Periodic Evolution | Every 100 rounds |
| Player Adaptation | Player changes pattern |

### Mutation Types

#### 1. Add Action

```python
# Original
["trap", "ambush"]

# Mutated
["trap", "ambush", "retreat"]
```

#### 2. Remove Action

```python
# Original
["trap", "wait", "ambush"]

# Mutated
["trap", "ambush"]
```

#### 3. Swap Action

```python
# Original
["defend", "attack"]

# Mutated
["defend", "psychological_bluff"]
```

#### 4. Hybrid Strategy

```python
# Combine two strategies
trap_strategy + ambush_strategy

# Creates
hybrid_trap_ambush_strategy
```

### Mutation Implementation

```python
def mutate(strategy, mutation_type, strength=0.1):
    """Apply mutation to strategy."""
    
    if mutation_type == "add_action":
        return add_random_action(strategy)
    
    elif mutation_type == "remove_action":
        return remove_action(strategy)
    
    elif mutation_type == "swap_action":
        return swap_action(strategy)
    
    elif mutation_type == "hybrid":
        return create_hybrid(strategy)
    
    return strategy
```

---

## Strategy Selection

The decision engine selects strategies based on multiple factors.

### Selection Algorithm

```python
def select_strategy(context, strategies, personality):
    """Select best strategy for current context."""
    
    scores = []
    
    for strategy in strategies:
        # Base score from effectiveness
        score = strategy["effectiveness"]
        
        # Apply personality modifiers
        if personality["aggression"] > 0.7:
            score += strategy["aggression_bonus"]
        
        if personality["caution"] > 0.7:
            score += strategy["defensive_bonus"]
        
        # Add randomness (chaos factor)
        score += random.random() * personality["chaos"] * 0.1
        
        # Consider context
        if context["player_aggressive"]:
            score += strategy["anti_aggressive_bonus"]
        
        scores.append((strategy, score))
    
    # Return highest scoring
    return max(scores, key=lambda x: x[1])[0]
```

---

## Memory System

**Location:** `aivill/memory/`

Stores learned information.

### Data Types

| Type | Description | Persistence |
|------|-------------|-------------|
| Player Profiles | Behavior patterns | Permanent |
| Strategy Memory | Effectiveness scores | Permanent |
| Short-term | Current game events | Session |
| Event Log | All interactions | Debug |

### Storage Format

```json
{
  "players": {
    "hero_001": {
      "action_frequency": {...},
      "games_played": 10,
      "behavior_patterns": {...}
    }
  },
  "strategies": {
    "aggressive_rush": {
      "effectiveness": 0.65,
      "use_count": 42,
      "success_count": 27
    }
  }
}
```

---

## Learning Configuration

### Adjustable Parameters

```python
config = {
    "learning": {
        "learning_rate": 0.1,      # How fast to learn (0-1)
        "discount_factor": 0.9,    # Future reward importance
        "exploration_rate": 0.1,    # Random action chance
        "min_effectiveness": 0.3,  # Don't use below this
        "mutation_rate": 0.1        # How often to mutate
    }
}
```

### Tuning Guidelines

| Parameter | Increase for | Decrease for |
|-----------|--------------|--------------|
| learning_rate | Faster adaptation | More stability |
| exploration_rate | More variety | More consistent |
| mutation_rate | More innovation | Less change |

---

## Observable Behavior

The learning system creates **visible adaptation**:

### Examples

| Player Behavior | Villain Adaptation |
|-----------------|-------------------|
| Always attacks early | Uses defensive traps |
| Escapes when low HP | Sets ambush at escape routes |
| Uses same path | Places traps along path |
| Avoids traps | Switches to direct attacks |
| Group fights | Uses area attacks |

### Player Feedback

```python
# After several games
profile = engine.get_player_profile(player_id)

print(f"You tend to {profile['most_common_action']} first")
print(f"When losing, you {profile['desperation_behavior']}")
print(f"You've won {profile['win_rate']} of our battles")
```

---

## Future Enhancements

Planned learning features:

- [ ] Deep Q-Networks (DQN)
- [ ] Monte Carlo Tree Search
- [ ] Neural network策略 evaluation
- [ ] Transfer learning between games
- [ ] Opponent modeling
- [ ] Multi-agent learning
- [ ] Evolutionary algorithms

---

## Research Questions

AiVill explores interesting research problems:

1. **Emergent Complexity** — Can simple rules create complex behavior?
2. **Player Modeling** — How accurately can we predict players?
3. **Adaptation Speed** — Optimal learning rates for engagement?
4. **Personality Emergence** — Do villains develop unique personalities?
5. **Engagement Balance** — When does learning improve vs frustrate?
