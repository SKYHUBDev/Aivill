"""
Player Pattern Test - Test AiVill's ability to detect player patterns

This experiment tests how well AiVill can identify and predict
player behavior patterns.
"""

import random
from aivill import VillainEngine


def run_pattern_detection_demo():
    """Test pattern detection."""
    print("=" * 60)
    print("AiVill Pattern Detection Experiment")
    print("=" * 60)
    
    # Create villain
    engine = VillainEngine({
        "name": "Pattern Detective",
        "data_dir": "data",
        "log_dir": "logs",
        "llm_model": None,
    })
    engine.load_personality({
        "traits": {
            "aggression": 0.5,
            "patience": 0.7,
            "ego": 0.5,
            "chaos": 0.1,
            "adaptability": 0.9,
            "caution": 0.5
        }
    })
    
    # Define player patterns to test
    patterns = {
        "aggressive": ["attack"] * 8 + ["defend"] * 1 + ["hide"] * 1,
        "defensive": ["attack"] * 2 + ["defend"] * 6 + ["hide"] * 2,
        "evasive": ["attack"] * 1 + ["defend"] * 3 + ["hide"] * 4 + ["explore"] * 2,
        "mixed": ["attack", "defend", "explore", "hide"] * 6 + ["negotiate"] * 4
    }
    
    results = {}
    
    for pattern_name, actions in patterns.items():
        print(f"\n--- Testing {pattern_name.upper()} player ---")
        
        # Reset engine for new pattern
        engine = VillainEngine({
            "name": f"Detector vs {pattern_name}",
            "data_dir": "data",
            "log_dir": "logs",
            "llm_model": None,
        })
        engine.load_personality({
            "traits": {
                "aggression": 0.5,
                "patience": 0.7,
                "ego": 0.5,
                "chaos": 0.1,
                "adaptability": 0.9,
                "caution": 0.5
            }
        })
        
        # Train for 30 rounds
        correct_predictions = 0
        for round_num in range(30):
            player_action = random.choice(actions)
            
            engine.update_state({
                "player_health": 80,
                "villain_health": 100,
                "player_last_action": player_action,
                "round_number": round_num + 1
            })
            
            decision = engine.decide_action()
            
            # Random outcome
            outcome = random.choice(["victory", "defeat", "draw"])
            engine.learn_from_result({
                "outcome": outcome,
                "success": outcome == "victory"
            })
        
        # Get player profile
        profile = engine.get_player_profile("default")
        
        if profile:
            print(f"  Detected patterns:")
            if 'action_frequency' in profile:
                for action, freq in sorted(profile['action_frequency'].items(), key=lambda x: -x[1]):
                    print(f"    {action}: {freq:.1%}")
            if 'behavior_patterns' in profile:
                for pattern, value in profile['behavior_patterns'].items():
                    if value:
                        print(f"    {pattern}: {value}")
        else:
            print("  (Profile learning in progress)")
        
        # Test prediction
        test_action = random.choice(actions)
        engine.update_state({
            "player_health": 80,
            "villain_health": 100,
            "player_last_action": test_action,
            "round_number": 31
        })
        
        summary = engine.get_state_summary()
        print(f"  Villain chose: {summary['strategy']['current']}")
        
        results[pattern_name] = "Learning complete"
    
    print("\n" + "=" * 60)
    print("Pattern Detection Summary")
    print("=" * 60)
    for pattern, result in results.items():
        print(f"  {pattern}: {result}")


if __name__ == "__main__":
    run_pattern_detection_demo()
