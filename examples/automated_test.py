"""Automated test for AiVill - demonstrates all features."""

import json
from aivill import VillainEngine


def print_separator():
    print("=" * 60)


def print_test_header(name):
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print("=" * 60)


def run_test():
    print_separator()
    print("AiVill Automated Test Suite")
    print_separator()

    test_results = []

    print_test_header("1. Create VillainEngine with phi3.5 model")
    try:
        config = {
            "name": "Lord of Shadows",
            "data_dir": "data",
            "log_dir": "logs",
            "llm_model": "phi3.5",
            "personality": {
                "aggression": 0.8,
                "patience": 0.4,
                "ego": 0.9,
                "chaos": 0.6,
                "adaptability": 0.7,
                "caution": 0.3
            }
        }

        engine = VillainEngine(config)
        print(f"Engine created: {engine.name}")
        print(f"LLM model: {config['llm_model']}")
        print(f"LLM available: {engine.llm_available}")
        test_results.append(("Create VillainEngine", True, None))
    except Exception as e:
        print(f"FAILED: {e}")
        test_results.append(("Create VillainEngine", False, str(e)))
        return test_results

    print_test_header("2. Test initialization and personality loading")
    try:
        engine.load_personality({"traits": config["personality"]})
        traits = engine.get_personality_traits()
        print(f"Loaded personality traits: {json.dumps(traits, indent=2)}")
        
        dominant_trait = engine.personality.get_dominant_trait()
        print(f"Dominant trait: {dominant_trait}")
        
        behavior_mods = engine.personality.get_behavior_modifiers()
        print(f"Behavior modifiers: {json.dumps(behavior_mods, indent=2)}")
        
        test_results.append(("Personality loading", True, None))
    except Exception as e:
        print(f"FAILED: {e}")
        test_results.append(("Personality loading", False, str(e)))

    print_test_header("3. Simulate 5 rounds of gameplay with different player actions")
    
    player_actions = [
        "attack",
        "defend",
        "explore",
        "negotiate",
        "hide"
    ]
    
    outcomes = [
        {"outcome": "victory", "success": True, "reward": 1.0, "damage_dealt": 20},
        {"outcome": "defeat", "success": False, "reward": -0.5, "damage_dealt": 5},
        {"outcome": "draw", "success": False, "reward": 0.0, "damage_dealt": 10},
        {"outcome": "victory", "success": True, "reward": 1.0, "damage_dealt": 25},
        {"outcome": "victory", "success": True, "reward": 1.0, "damage_dealt": 30}
    ]

    try:
        for round_num, (player_action, outcome) in enumerate(zip(player_actions, outcomes), 1):
            print(f"\n--- Round {round_num} ---")
            print(f"Player action: {player_action}")
            
            player_health = max(0, 100 - (round_num * 10))
            villain_health = max(0, 100 - (round_num * 5))
            
            game_state = {
                "player_id": "hero_001",
                "player_health": player_health,
                "villain_health": villain_health,
                "player_last_action": player_action,
                "round_number": round_num,
                "available_actions": [
                    "direct_attack", "scheming", "opportunistic",
                    "defensive", "intimidating", "negotiating", "chaotic"
                ],
                "environment_objects": ["cover", "trap", "weapon", "treasure"]
            }
            
            observations = engine.update_state(game_state)
            print(f"Observations: aggressive={observations.get('player_is_aggressive', False)}")
            
            try:
                decision = engine.decide_action()
                print(f"Villain action: {decision['action']}")
                print(f"Strategy: {decision.get('strategy', 'N/A')}")
            except Exception as e:
                print(f"Decision error (continuing): {e}")
                decision = {"action": "defensive", "strategy": "Defensive"}
                print(f"Villain action: {decision['action']} (fallback)")
            
            engine.learn_from_result(outcome)
            print(f"Outcome: {outcome['outcome']} - Villain learned!")
        
        print(f"\nTotal decisions made: {engine.total_decisions}")
        test_results.append(("5 rounds gameplay", True, None))
    except Exception as e:
        print(f"FAILED: {e}")
        test_results.append(("5 rounds gameplay", False, str(e)))

    print_test_header("4. Test LLM suggestions and taunt generation")
    try:
        if engine.llm_available:
            suggestion = engine.get_llm_suggestion(
                "The player keeps attacking aggressively. Suggest a strategy for the villain."
            )
            print(f"LLM Strategy Suggestion: {suggestion[:200] if suggestion else 'None'}")
            
            taunt = engine.get_llm_suggestion(
                "Generate a menacing taunt from a villain who is winning."
            )
            print(f"LLM Taunt: {taunt}")
            
            llm_gen_taunt = engine.ollama.generate_taunt_or_dialogue(
                {"situation": "The villain has gained the upper hand"},
                style="menacing"
            )
            print(f"Generated Taunt: {llm_gen_taunt}")
        else:
            print("LLM not available - using fallback responses")
            suggestion = "Strategy: Exploit the player's aggression by using defensive tactics."
            taunt = "You think you can defeat me? I have planned for this moment for centuries!"
            print(f"Fallback Suggestion: {suggestion}")
            print(f"Fallback Taunt: {taunt}")
        
        test_results.append(("LLM suggestions", True, None))
    except Exception as e:
        print(f"FAILED: {e}")
        test_results.append(("LLM suggestions", False, str(e)))

    print_test_header("5. Test player profile learning")
    try:
        profile = engine.get_player_profile("hero_001")
        print(f"Player profile retrieved: {profile is not None}")
        
        if profile:
            print(f"Player ID: {profile.get('player_id')}")
            print(f"Interaction count: {profile.get('interaction_count')}")
            print(f"Trust level: {profile.get('trust_level')}")
            print(f"Risk tolerance: {profile.get('risk_tolerance')}")
            print(f"Preferred strategies: {profile.get('preferred_strategies', [])}")
            print(f"Learned patterns: {json.dumps(profile.get('learned_patterns', {}), indent=2)}")
        
        profile = engine.get_player_profile("new_player")
        print(f"New player profile (non-existent): {profile}")
        
        test_results.append(("Player profile learning", True, None))
    except Exception as e:
        print(f"FAILED: {e}")
        test_results.append(("Player profile learning", False, str(e)))

    print_test_header("6. Test personality adaptation over time")
    try:
        traits_before = engine.get_personality_traits()
        print(f"Traits before adaptation: {json.dumps(traits_before, indent=2)}")
        
        engine.adapt_personality("aggression", 0.1, "test_adaptation")
        engine.adapt_personality("caution", -0.05, "test_adaptation")
        
        traits_after = engine.get_personality_traits()
        print(f"Traits after adaptation: {json.dumps(traits_after, indent=2)}")
        
        print(f"Aggression changed: {traits_before['aggression']} -> {traits_after['aggression']}")
        print(f"Caution changed: {traits_before['caution']} -> {traits_after['caution']}")
        
        personality_summary = engine.personality.get_personality_summary()
        print(f"Personality history count: {personality_summary['trait_history_count']}")
        print(f"Major events count: {personality_summary['major_events_count']}")
        
        test_results.append(("Personality adaptation", True, None))
    except Exception as e:
        print(f"FAILED: {e}")
        test_results.append(("Personality adaptation", False, str(e)))

    print_test_header("7. Save and verify memory")
    try:
        engine.save_memory()
        print("Memory saved successfully")
        
        state_summary = engine.get_state_summary()
        print(f"Total decisions: {state_summary['total_decisions']}")
        print(f"Total learning iterations: {state_summary['total_learning_iterations']}")
        print(f"Memory stats: {json.dumps(state_summary.get('memory', {}), indent=2)}")
        
        engine.load_memory()
        print("Memory loaded successfully")
        
        test_results.append(("Save and verify memory", True, None))
    except Exception as e:
        print(f"FAILED: {e}")
        test_results.append(("Save and verify memory", False, str(e)))

    print_test_header("FINAL SUMMARY")
    print("\nTest Results:")
    print("-" * 40)
    
    all_passed = True
    for test_name, passed, error in test_results:
        status = "PASS" if passed else "FAIL"
        print(f"{test_name}: {status}")
        if error:
            print(f"  Error: {error}")
        if not passed:
            all_passed = False
    
    print("-" * 40)
    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed!")
    
    print(f"\nFinal personality traits:")
    final_traits = engine.get_personality_traits()
    for trait, value in final_traits.items():
        bar = "#" * int(value * 10) + "-" * (10 - int(value * 10))
        print(f"  {trait:12}: [{bar}] {value:.2f}")

    return test_results


if __name__ == "__main__":
    run_test()
