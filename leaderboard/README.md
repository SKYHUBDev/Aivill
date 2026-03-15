# AiVill Villain Leaderboard

Welcome to the AiVill Villain Leaderboard! This is where the community submits and ranks their most effective adaptive villain strategies.

## Top Adaptive Villains

| Rank | Name | Strategy | Win Rate | Rounds |
|------|------|----------|----------|--------|
| 1 | trap_master_v2 | adaptive_trap_strategy | 91% | 100 |
| 2 | chaos_overlord | chaos_manipulation | 86% | 100 |
| 3 | mind_reader | predictive_counter | 82% | 100 |
| 4 | aggressive_berserker | rush_strategy | 78% | 100 |
| 5 | defensive_turtle | fortress_strategy | 65% | 100 |

## Submit Your Villain

### How to Submit

1. **Create your villain** using AiVill's personality system
2. **Test it** for at least 50 rounds
3. **Record the results** including:
   - Villain name
   - Strategy description
   - Win rate
   - Rounds tested
   - Personality configuration

### Submission Format

```python
from leaderboard import VillainLeaderboard

leaderboard = VillainLeaderboard()
leaderboard.add_entry(
    villain_name="your_villain_name",
    strategy="your_strategy_description",
    win_rate=0.75,  # 75% win rate
    rounds_tested=50,
    personality={
        "aggression": 0.6,
        "patience": 0.4,
        "ego": 0.7,
        "chaos": 0.3,
        "adaptability": 0.8,
        "caution": 0.5
    },
    description="Your villain's strategy description"
)
```

### Evaluation Criteria

Villains are ranked by:

- **Win Rate** (primary) - Percentage of rounds won
- **Rounds Tested** - More rounds = more reliable
- **Innovation** - Unique strategies get bonus recognition

## Leaderboard Rules

1. Minimum 50 rounds required for submission
2. All rounds must be from valid gameplay
3. Submit one entry per strategy
4. Updates replace previous entries

## Current Challenge

### This Month's Challenge: "The Adaptive Assassin"

Create a villain that:
- Learns player's favorite escape routes
- Adapts within 10 rounds
- Achieves 80%+ win rate

Submit your entry by opening a pull request!

## Community

Join the discussion:
- Share strategies on GitHub Issues
- Post your results in Discussions
- Challenge other players' villains

## See Also

- [Experiment Playground](../experiments/README.md)
- [Villain Personality Generator](../villains/README.md)
- [API Documentation](../docs/engine_api.md)
