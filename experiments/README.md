# AiVill Experiment Playground

Welcome to the AiVill Experiment Playground! This directory contains runnable experiments that demonstrate the learning and adaptation capabilities of AiVill's adaptive villain AI.

## Quick Start

```bash
# Run learning demo
python experiments/learning_demo.py

# Run strategy evolution demo
python experiments/strategy_evolution_demo.py

# Run pattern detection demo
python experiments/player_pattern_test.py
```

## Available Experiments

### 1. Learning Demo (`learning_demo.py`)

**What it demonstrates:**
- How AiVill learns from predictable player behavior
- The villain's win rate improvement over time
- Personality trait evolution based on outcomes

**Scenario:**
- Player attacks 70% of the time
- Villain starts with no knowledge
- Watch as the villain adapts its strategy

**Expected output:**
```
Round 10: win rate = 0.46
Round 20: win rate = 0.71
Round 30: win rate = 0.84
```

### 2. Strategy Evolution Demo (`strategy_evolution_demo.py`)

**What it demonstrates:**
- How AiVill mutates and evolves strategies
- Strategy effectiveness changes over time
- Adaptation to varying player behaviors

**Scenario:**
- Player uses varying strategies
- Villain's strategies evolve to counter
- Track strategy mutations

### 3. Player Pattern Test (`player_pattern_test.py`)

**What it demonstrates:**
- Pattern detection in player behavior
- Prediction of player actions
- Profile building from experience

**Scenario:**
- Test with different player archetypes:
  - Aggressive (80% attack)
  - Defensive (60% defend)
  - Evasive (40% hide)
  - Mixed (varied)

## Adding Your Own Experiments

Want to create your own experiment? Here's how:

### Template

```python
from aivill import VillainEngine

# 1. Create engine
engine = VillainEngine({
    "name": "Your Experiment",
    "data_dir": "data",
    "log_dir": "logs",
    "llm_model": None
})

# 2. Set personality
engine.load_personality({
    "traits": {
        "aggression": 0.5,
        "patience": 0.5,
        "ego": 0.5,
        "chaos": 0.2,
        "adaptability": 0.8,
        "caution": 0.5
    }
})

# 3. Run experiment loop
for round_num in range(100):
    # Update state
    engine.update_state({
        "player_health": 80,
        "villain_health": 100,
        "player_last_action": "attack",
        "round_number": round_num + 1
    })
    
    # Get decision
    decision = engine.decide_action()
    
    # Learn result
    engine.learn_from_result({
        "outcome": "victory",
        "success": True
    })

# 4. Analyze results
print(engine.get_state_summary())
```

### Experiment Ideas

Here are some ideas for experiments:

1. **Learning Speed Test** - Compare different adaptability settings
2. **Personality Impact** - Test how different personalities affect outcomes
3. **Strategy Comparison** - Test different starting strategies
4. **Multiplayer Adaptation** - Test against multiple player types
5. **Long-term Evolution** - Run thousands of rounds to see long-term behavior

## Research Questions

These experiments explore open questions in adaptive game AI:

- **Emergent Behavior** - Can simple rules create complex strategies?
- **Learning Speed** - What's the optimal adaptability rate?
- **Player Modeling** - How accurately can we predict players?
- **Personality Stability** - Do villains develop consistent personalities?
- **Engagement Balance** - When does learning improve vs frustrate?

## Contributing

Share your experiments! Open a pull request to add your experiment to this directory.

## See Also

- [API Documentation](../docs/engine_api.md)
- [Learning System](../docs/learning_system.md)
- [Villain Leaderboard](../leaderboard/README.md)
```
