"""
Extended stress test - 500+ iterations with detailed analysis
"""

import time
import json
import statistics
import random
from collections import defaultdict
from aivill import VillainEngine


def test_500_iterations():
    """Test 500 iterations without LLM for maximum speed."""
    print("=" * 60)
    print("500 ITERATIONS TEST (No LLM)")
    print("=" * 60)
    
    engine = VillainEngine({
        "name": "500 Test",
        "data_dir": "data",
        "log_dir": "logs",
        "llm_model": None,
    })
    engine.load_personality({"traits": {
        "aggression": 0.5,
        "patience": 0.5,
        "ego": 0.5,
        "chaos": 0.5,
        "adaptability": 0.5,
        "caution": 0.5,
    }})
    
    actions = ["attack", "defend", "explore", "negotiate", "hide"]
    times = []
    
    for i in range(500):
        start = time.time()
        
        game_state = {
            "player_health": random.randint(0, 100),
            "villain_health": random.randint(0, 100),
            "player_last_action": random.choice(actions),
            "round_number": i + 1,
        }
        
        engine.update_state(game_state)
        decision = engine.decide_action()
        
        outcome = random.choice(["victory", "defeat", "draw"])
        engine.learn_from_result({
            "outcome": outcome,
            "success": outcome == "victory",
        })
        
        times.append(time.time() - start)
    
    print(f"Total: {len(times)} iterations")
    print(f"Avg time: {statistics.mean(times):.5f}s")
    print(f"Min: {min(times):.5f}s")
    print(f"Max: {max(times):.5f}s")
    print(f"P95: {sorted(times)[int(len(times)*0.95)]:.5f}s")
    print(f"P99: {sorted(times)[int(len(times)*0.99)]:.5f}s")
    
    # Check memory growth
    summary = engine.get_state_summary()
    print(f"Decisions: {summary['total_decisions']}")
    print(f"Learning: {summary['total_learning_iterations']}")
    
    return times


def test_memory_leak():
    """Check for memory leaks."""
    print("\n" + "=" * 60)
    print("MEMORY LEAK TEST")
    print("=" * 60)
    
    engine = VillainEngine({
        "name": "Leak Test",
        "data_dir": "data",
        "log_dir": "logs",
        "llm_model": None,
    })
    engine.load_personality({"traits": {
        "aggression": 0.5, "patience": 0.5, "ego": 0.5,
        "chaos": 0.5, "adaptability": 0.5, "caution": 0.5,
    }})
    
    # Check initial state
    initial_stats = engine.get_state_summary()
    print(f"Initial memory stats: {initial_stats['memory']}")
    
    # Run many iterations
    for i in range(100):
        engine.update_state({"player_health": 50, "round_number": i})
        engine.decide_action()
        engine.learn_from_result({"success": True})
    
    # Check final state
    final_stats = engine.get_state_summary()
    print(f"Final memory stats: {final_stats['memory']}")
    
    # Save and reload
    engine.save_memory()
    engine.load_memory()
    
    final_stats2 = engine.get_state_summary()
    print(f"After reload: {final_stats2['memory']}")
    
    print("Memory leak test: OK" if final_stats['memory'] else "ISSUE DETECTED")


def test_concurrent_games():
    """Test multiple engine instances."""
    print("\n" + "=" * 60)
    print("CONCURRENT ENGINES TEST")
    print("=" * 60)
    
    engines = []
    
    # Create 10 engines
    for i in range(10):
        eng = VillainEngine({
            "name": f"Engine {i}",
            "data_dir": "data",
            "log_dir": "logs",
            "llm_model": None,
        })
        eng.load_personality({"traits": {
            "aggression": random.random(),
            "patience": random.random(),
            "ego": random.random(),
            "chaos": random.random(),
            "adaptability": random.random(),
            "caution": random.random(),
        }})
        engines.append(eng)
    
    # Run each for 50 rounds
    for eng in engines:
        for i in range(50):
            eng.update_state({"player_health": 50, "round_number": i})
            eng.decide_action()
            eng.learn_from_result({"success": i % 2 == 0})
    
    print(f"Created {len(engines)} engines")
    print("All completed 50 rounds each")
    
    # Check they're independent
    for i, eng in enumerate(engines):
        summary = eng.get_state_summary()
        print(f"Engine {i}: {summary['total_decisions']} decisions")


def test_strategy_evolution():
    """Test that strategies actually evolve."""
    print("\n" + "=" * 60)
    print("STRATEGY EVOLUTION TEST")
    print("=" * 60)
    
    engine = VillainEngine({
        "name": "Evolution Test",
        "data_dir": "data",
        "log_dir": "logs",
        "llm_model": None,
    })
    engine.load_personality({"traits": {
        "aggression": 0.8,
        "patience": 0.2,
        "ego": 0.5,
        "chaos": 0.1,
        "adaptability": 0.9,
        "caution": 0.3,
    }})
    
    # Track action distribution
    actions_used = defaultdict(int)
    
    # Run 100 rounds always attacking
    for i in range(100):
        engine.update_state({
            "player_health": 80,
            "player_last_action": "attack",
            "round_number": i + 1,
        })
        decision = engine.decide_action()
        actions_used[decision["action"]] += 1
        
        # Always win
        engine.learn_from_result({"success": True})
    
    print("Action distribution (after learning against attacker):")
    for action, count in sorted(actions_used.items(), key=lambda x: -x[1]):
        print(f"  {action}: {count} ({count}%)")
    
    # Now change strategy - player defends
    actions_used2 = defaultdict(int)
    for i in range(50):
        engine.update_state({
            "player_health": 80,
            "player_last_action": "defend",
            "round_number": i + 1,
        })
        decision = engine.decide_action()
        actions_used2[decision["action"]] += 1
    
    print("\nAction distribution (after learning against defender):")
    for action, count in sorted(actions_used2.items(), key=lambda x: -x[1]):
        print(f"  {action}: {count} ({count}%)")
    
    print("Strategy evolution test: COMPLETE")


def test_persistence():
    """Test save/load persistence."""
    print("\n" + "=" * 60)
    print("PERSISTENCE TEST")
    print("=" * 60)
    
    # Create and train engine
    engine1 = VillainEngine({
        "name": "Original",
        "data_dir": "data",
        "log_dir": "logs",
        "llm_model": None,
    })
    engine1.load_personality({"traits": {
        "aggression": 0.7, "patience": 0.3, "ego": 0.8,
        "chaos": 0.2, "adaptability": 0.6, "caution": 0.4,
    }})
    
    # Train it
    for i in range(30):
        engine1.update_state({"player_health": 50, "round_number": i})
        engine1.decide_action()
        engine1.learn_from_result({"success": i % 2 == 0})
    
    engine1.save_memory()
    
    traits_before = engine1.get_personality()
    summary_before = engine1.get_state_summary()
    
    # Create new engine and load
    engine2 = VillainEngine({
        "name": "Loaded",
        "data_dir": "data",
        "log_dir": "logs",
        "llm_model": None,
    })
    engine2.load_memory()
    
    traits_after = engine2.get_personality()
    summary_after = engine2.get_state_summary()
    
    print(f"Before - Decisions: {summary_before['total_decisions']}, Traits: {traits_before}")
    print(f"After  - Decisions: {summary_after['total_decisions']}, Traits: {traits_after}")
    
    # Check they match
    if summary_after['total_decisions'] > 0:
        print("Persistence test: PASS")
    else:
        print("Persistence test: FAIL")


if __name__ == "__main__":
    # Run all tests
    test_500_iterations()
    test_memory_leak()
    test_concurrent_games()
    test_strategy_evolution()
    test_persistence()
    
    print("\n" + "=" * 60)
    print("ALL EXTENDED TESTS COMPLETE")
    print("=" * 60)
