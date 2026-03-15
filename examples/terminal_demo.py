"""
Terminal demo - Interactive demonstration of AiVill with LLM-powered villain.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
from aivill import VillainEngine


def print_separator():
    print("=" * 60)


def print_menu():
    print("\n--- Main Menu ---")
    print("1. Start New Game")
    print("2. Continue Existing Game")
    print("3. View Villain Status")
    print("4. View Player Profile")
    print("5. Get LLM Strategy Suggestion")
    print("6. Generate Villain Taunt")
    print("7. Exit")


def create_engine():
    """Create and initialize the VillainEngine."""
    config = {
        "name": "Lord of Shadows",
        "data_dir": "data",
        "log_dir": "logs",
        "llm_model": "phi3.5",  # Using phi3.5 for reasoning
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
    
    # Load personality
    engine.load_personality({"traits": config["personality"]})
    
    return engine


def play_round(engine, round_num):
    """Play a single round."""
    print(f"\n--- Round {round_num} ---")
    
    # Get player action
    print("\nPlayer actions: attack, defend, explore, negotiate, hide")
    player_action = input("Player action: ").strip().lower()
    
    # Simulate game state
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
    
    # Update state and get observations
    observations = engine.update_state(game_state)
    print(f"\nVillain perceives: {observations.get('player_is_aggressive', False) and 'Player is aggressive' or 'Player is cautious'}")
    
    # Get villain decision
    decision = engine.decide_action()
    print(f"\n>>> Villain chooses: {decision['action'].upper()}")
    print(f"    Strategy: {decision['strategy']}")
    
    # Show LLM reasoning if available
    if engine.llm_available:
        print(f"    [LLM Active: Yes]")
    
    # Get result from player
    print("\nOutcome: win, lose, or neutral?")
    outcome = input("Result: ").strip().lower()
    
    result_map = {
        "win": {"outcome": "victory", "success": True, "reward": 1.0},
        "lose": {"outcome": "defeat", "success": False, "reward": -1.0},
        "neutral": {"outcome": "draw", "success": False, "reward": 0.0}
    }
    
    result = result_map.get(outcome, {"outcome": "unknown", "success": False, "reward": 0.0})
    result["damage_dealt"] = 20 if outcome == "win" else 5
    result["damage_received"] = 5 if outcome == "win" else 20
    
    # Learn from result
    engine.learn_from_result(result)
    print(f"    Villain learned from {outcome}!")
    
    return player_health, villain_health


def main():
    print_separator()
    print("  AiVill - Self-Learning Villain Brain AI")
    print("  Powered by Ollama (phi3.5)")
    print_separator()
    
    engine = create_engine()
    
    print(f"\nInitialized: {engine.name}")
    print(f"LLM Available: {engine.llm_available}")
    
    if engine.llm_available:
        print(">>> Using phi3.5 for strategy suggestions and dialogue")
    
    # Show initial personality
    traits = engine.get_personality()
    print("\nInitial Personality:")
    for trait, value in traits.items():
        bar = "#" * int(value * 10) + "-" * (10 - int(value * 10))
        print(f"  {trait:12}: [{bar}] {value:.2f}")
    
    game_active = True
    round_num = 0
    
    while game_active:
        print_menu()
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            # Start new game
            round_num = 0
            player_hp = 100
            villain_hp = 100
            
            print("\n=== NEW GAME STARTED ===")
            
            while player_hp > 0 and villain_hp > 0:
                round_num += 1
                player_hp, villain_hp = play_round(engine, round_num)
                
                if player_hp <= 0:
                    print("\n*** PLAYER DEFEATED! ***")
                    print("The villain wins!")
                elif villain_hp <= 0:
                    print("\n*** VILLAIN DEFEATED! ***")
                    print("The hero prevails!")
                
                cont = input("\nContinue? (y/n): ").strip().lower()
                if cont != 'y':
                    break
            
            engine.save_memory()
            print("\nMemory saved!")
            
        elif choice == "2":
            # Continue game
            round_num += 1
            play_round(engine, round_num)
            engine.save_memory()
            
        elif choice == "3":
            # View villain status
            summary = engine.get_state_summary()
            print_separator()
            print("  VILLAIN STATUS")
            print_separator()
            print(f"Name: {summary['name']}")
            print(f"Total Decisions: {summary['total_decisions']}")
            print(f"LLM Available: {summary['llm_available']}")
            print("\nPersonality:")
            for trait, value in summary['personality'].items():
                bar = "#" * int(value * 10) + "-" * (10 - int(value * 10))
                print(f"  {trait:12}: [{bar}] {value:.2f}")
            
        elif choice == "4":
            # View player profile
            profile = engine.get_player_profile("hero_001")
            print_separator()
            print("  PLAYER PROFILE")
            print_separator()
            if profile:
                print(json.dumps(profile, indent=2))
            else:
                print("No profile found yet. Play some rounds first!")
            
        elif choice == "5":
            # LLM suggestion
            if not engine.llm_available:
                print("\nLLM not available. Make sure Ollama is running.")
            else:
                prompt = """The player keeps attacking aggressively. 
Suggest a strategy for the villain to counter this."""
                suggestion = engine.get_llm_suggestion(prompt)
                print_separator()
                print("  LLM STRATEGY SUGGESTION")
                print_separator()
                print(suggestion)
            
        elif choice == "6":
            # Generate taunt
            if not engine.llm_available:
                print("\nLLM not available. Make sure Ollama is running.")
            else:
                taunt = engine.get_llm_suggestion(
                    "Generate a menacing taunt from a villain who is winning against an aggressive player."
                )
                print_separator()
                print("  VILLAIN TAUNT")
                print_separator()
                print(f'"{taunt}"')
            
        elif choice == "7":
            # Exit
            engine.save_memory()
            print("\nMemory saved. Farewell, Villain Mastermind!")
            game_active = False
            
        else:
            print("\nInvalid option. Please try again.")
    
    print_separator()


if __name__ == "__main__":
    main()
