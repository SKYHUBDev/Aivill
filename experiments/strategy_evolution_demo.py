"""
Strategy Evolution Demo - Show how AiVill mutates strategies

This experiment demonstrates how the villain's strategies evolve over time
through mutation and adaptation.
"""

import random
from aivill import VillainEngine


def run_strategy_evolution_demo():
    """Demonstrate strategy evolution."""
    print("=" * 60)
    print("AiVill Strategy Evolution Experiment")
    print("=" * 60)
    
    # Create villain
    engine = VillainEngine({
        "name": "Evolution Villain",
        "data_dir": "data",
        "log_dir": "logs",
        "llm_model": None,
    })
    engine.load_personality({
        "traits": {
            "aggression": 0.6,
            "patience": 0.5,
            "ego": 0.5,
            "chaos": 0.4,
            "adaptability": 0.9,
            "caution": 0.4
        }
    })
    
    print("\nInitial Strategy:")
    initial = engine.get_state_summary()
    print(f"  Current: {initial['strategy']['current']}")
    print(f"  Effectiveness: {initial['strategy']['effectiveness']:.2f}")
    print(f"  Uses: {initial['strategy']['uses']}")
    
    print("\n" + "-" * 60)
    print("Running 100 rounds to trigger evolution...")
    print("-" * 60 + "\n")
    
    # Run rounds with varying player behavior to trigger mutations
    player_actions = ["attack", "defend", "explore", "hide", "negotiate"]
    
    for i in range(100):
        player_action = random.choice(player_actions)
        
        engine.update_state({
            "player_health": 80 - i,
            "villain_health": 100 - i,
            "player_last_action": player_action,
            "round_number": i + 1
        })
        
        decision = engine.decide_action()
        
        # Alternate between wins and losses to encourage adaptation
        outcome = "victory" if i % 2 == 0 else "defeat"
        engine.learn_from_result({
            "outcome": outcome,
            "success": i % 2 == 0
        })
        
        # Print strategy changes
        if i > 0 and i % 20 == 0:
            summary = engine.get_state_summary()
            print(f"Round {i:3d}: Strategy = {summary['strategy']['current']}, "
                  f"Effectiveness = {summary['strategy']['effectiveness']:.2f}")
    
    print("\n" + "=" * 60)
    print("Final Strategy State:")
    final = engine.get_state_summary()
    print(f"  Current Strategy: {final['strategy']['current']}")
    print(f"  Effectiveness: {final['strategy']['effectiveness']:.2f}")
    print(f"  Total Uses: {final['strategy']['uses']}")
    
    print("\nStrategy History:")
    if 'strategy' in final and 'history' in final['strategy']:
        for strategy in final['strategy']['history'][-5:]:
            print(f"  - {strategy['name']}: {strategy['effectiveness']:.2f}")
    else:
        print("  (History not available)")


if __name__ == "__main__":
    run_strategy_evolution_demo()
