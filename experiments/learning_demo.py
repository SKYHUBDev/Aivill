"""
Learning Demo - Observe how AiVill learns from predictable player behavior

This experiment simulates a player with fixed behavior patterns and shows
how the villain adapts its strategy over time.

Expected result: Villain win rate should increase as it learns the player's patterns.
"""

import time
import random
from collections import defaultdict
from aivill import VillainEngine


def run_learning_demo():
    """Demonstrate learning behavior."""
    print("=" * 60)
    print("AiVill Learning Experiment")
    print("=" * 60)
    print("\nScenario: Player attacks 70% of the time")
    print("=" * 60)
    
    # Create villain with moderate personality
    engine = VillainEngine({
        "name": "Learning Villain",
        "data_dir": "data",
        "log_dir": "logs",
        "llm_model": None,  # No LLM for speed
    })
    engine.load_personality({
        "traits": {
            "aggression": 0.5,
            "patience": 0.5,
            "ego": 0.5,
            "chaos": 0.2,
            "adaptability": 0.8,  # High adaptability
            "caution": 0.5
        }
    })
    
    # Track results
    wins = 0
    losses = 0
    draws = 0
    win_rates = []
    
    # Player action probabilities (70% attack)
    player_actions = ["attack"] * 7 + ["defend"] * 2 + ["retreat"] * 1
    
    # Run 50 rounds
    print("\nRunning 50 rounds...")
    print("-" * 60)
    
    for round_num in range(1, 51):
        # Player chooses action based on probability
        player_action = random.choice(player_actions)
        
        # Update game state
        game_state = {
            "player_health": 100 - (round_num * 2),
            "villain_health": 100 - (round_num * 1),
            "player_last_action": player_action,
            "round_number": round_num
        }
        engine.update_state(game_state)
        
        # Get villain decision
        decision = engine.decide_action()
        
        # Simulate outcome
        # If player attacks and villain attacks -> both take damage (draw)
        # If player defends and villain attacks -> player takes more damage (win)
        # If player retreats and villain attacks -> player escapes (lose)
        
        if player_action == "attack":
            if decision["action"] in ["direct_attack", "intimidating"]:
                outcome = "draw"
                wins += 1
            elif decision["action"] == "defensive":
                outcome = "defeat"
                losses += 1
            else:
                outcome = "draw"
                draws += 1
        elif player_action == "defend":
            if decision["action"] in ["direct_attack", "intimidating"]:
                outcome = "victory"
                wins += 1
            else:
                outcome = "draw"
                draws += 1
        else:  # retreat
            outcome = "defeat"
            losses += 1
        
        # Learn from result
        engine.learn_from_result({
            "outcome": outcome,
            "success": outcome == "victory",
            "reward": 1.0 if outcome == "victory" else (-1.0 if outcome == "defeat" else 0.0)
        })
        
        # Record win rate every 10 rounds
        if round_num % 10 == 0:
            win_rate = wins / (wins + losses + draws)
            win_rates.append((round_num, win_rate))
            print(f"Round {round_num:2d}: win rate = {win_rate:.2f} ({wins}W/{losses}L/{draws}D)")
    
    print("-" * 60)
    print(f"\nFinal Statistics:")
    print(f"  Total Rounds: {wins + losses + draws}")
    print(f"  Wins: {wins} ({wins/50*100:.0f}%)")
    print(f"  Losses: {losses} ({losses/50*100:.0f}%)")
    print(f"  Draws: {draws} ({draws/50*100:.0f}%)")
    
    # Show personality evolution
    print(f"\nPersonality Evolution:")
    traits = engine.get_personality()
    for trait, value in traits.items():
        bar = "#" * int(value * 10) + "-" * (10 - int(value * 10))
        print(f"  {trait:12}: [{bar}] {value:.2f}")
    
    # Show learning summary
    summary = engine.get_state_summary()
    print(f"\nLearning Summary:")
    print(f"  Total Decisions: {summary['total_decisions']}")
    print(f"  Strategy: {summary['strategy'].get('current', 'N/A')}")
    effectiveness = summary['strategy'].get('effectiveness')
    print(f"  Effectiveness: {effectiveness if effectiveness is not None else 'N/A'}")
    
    return win_rates


if __name__ == "__main__":
    run_learning_demo()
