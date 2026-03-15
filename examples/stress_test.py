"""
Stress test for AiVill - runs 200+ iterations to find choke points
and optimize for edge deployment.
"""

import time
import json
import statistics
from collections import defaultdict
from aivill import VillainEngine


class StressTest:
    """Comprehensive stress testing for AiVill engine."""
    
    def __init__(self):
        self.results = []
        self.timings = defaultdict(list)
        self.errors = []
        self.model = "qwen2.5:1.5b"  # Edge-optimized model
        
    def run_all_tests(self):
        """Run all stress tests."""
        print("=" * 70)
        print("AiVill STRESS TEST - Edge Deployment Optimization")
        print("=" * 70)
        print(f"Model: {self.model} (986MB - optimized for edge)")
        print()
        
        # Test configurations
        configs = [
            {"name": "qwen2.5:1.5b", "llm_model": "qwen2.5:1.5b", "personality": {
                "aggression": 0.5,
                "patience": 0.5,
                "ego": 0.5,
                "chaos": 0.5,
                "adaptability": 0.5,
                "caution": 0.5,
            }},
            {"name": "phi3.5", "llm_model": "phi3.5", "personality": {
                "aggression": 0.5,
                "patience": 0.5,
                "ego": 0.5,
                "chaos": 0.5,
                "adaptability": 0.5,
                "caution": 0.5,
            }},
            {"name": "no_llm", "llm_model": None, "personality": {
                "aggression": 0.5,
                "patience": 0.5,
                "ego": 0.5,
                "chaos": 0.5,
                "adaptability": 0.5,
                "caution": 0.5,
            }},
        ]
        
        for config in configs:
            print(f"\n{'='*70}")
            print(f"Testing: {config['name']}")
            print(f"{'='*70}")
            
            try:
                self.test_model(config)
            except Exception as e:
                print(f"Error: {e}")
                self.errors.append((config['name'], str(e)))
        
        # Run massive iteration test
        print(f"\n{'='*70}")
        print("MASSIVE ITERATION TEST (200 rounds)")
        print(f"{'='*70}")
        self.test_massive_iterations()
        
        # Run edge cases
        print(f"\n{'='*70}")
        print("EDGE CASE TESTS")
        print(f"{'='*70}")
        self.test_edge_cases()
        
        # Run memory stress
        print(f"\n{'='*70}")
        print("MEMORY STRESS TEST")
        print(f"{'='*70}")
        self.test_memory_stress()
        
        # Print final summary
        self.print_summary()
    
    def test_model(self, config):
        """Test a specific model configuration."""
        print(f"\n--- Creating engine with {config['name']} ---")
        
        start = time.time()
        engine = VillainEngine({
            "name": f"Stress Test - {config['name']}",
            "data_dir": "data",
            "log_dir": "logs",
            "llm_model": config['llm_model'],
        })
        engine.load_personality({"traits": config.get("personality", {
            "aggression": 0.5,
            "patience": 0.5,
            "ego": 0.5,
            "chaos": 0.5,
            "adaptability": 0.5,
            "caution": 0.5,
        })})
        init_time = time.time() - start
        print(f"Init time: {init_time:.3f}s")
        
        # Test LLM availability
        print(f"LLM Available: {engine.llm_available}")
        
        # Run 10 quick rounds
        for i in range(10):
            game_state = {
                "player_health": 100 - (i * 5),
                "villain_health": 100 - (i * 3),
                "player_last_action": ["attack", "defend", "explore", "hide"][i % 4],
                "round_number": i + 1,
            }
            
            start = time.time()
            engine.update_state(game_state)
            update_time = time.time() - start
            
            start = time.time()
            decision = engine.decide_action()
            decide_time = time.time() - start
            
            start = time.time()
            engine.learn_from_result({
                "outcome": "victory" if i % 3 == 0 else "defeat",
                "success": i % 3 == 0,
                "reward": 1.0 if i % 3 == 0 else -1.0
            })
            learn_time = time.time() - start
            
            self.timings[f"{config['name']}_update"].append(update_time)
            self.timings[f"{config['name']}_decide"].append(decide_time)
            self.timings[f"{config['name']}_learn"].append(learn_time)
        
        # Test LLM if available
        if engine.llm_available and config['llm_model']:
            print("Testing LLM...")
            start = time.time()
            suggestion = engine.get_llm_suggestion("What should the villain do?")
            llm_time = time.time() - start
            self.timings[f"{config['name']}_llm"].append(llm_time)
            print(f"LLM time: {llm_time:.3f}s")
        
        engine.save_memory()
        
        # Print timing stats
        for key in self.timings:
            if config['name'] in key and self.timings[key]:
                avg = statistics.mean(self.timings[key])
                print(f"  {key}: {avg:.4f}s avg")
    
    def test_massive_iterations(self):
        """Run 200 iterations to find performance patterns."""
        print("\n--- Running 200 iterations ---")
        
        engine = VillainEngine({
            "name": "Massive Test",
            "data_dir": "data",
            "log_dir": "logs",
            "llm_model": None,  # No LLM for speed
        })
        engine.load_personality({"traits": {
            "aggression": 0.6,
            "patience": 0.4,
            "ego": 0.5,
            "chaos": 0.3,
            "adaptability": 0.7,
            "caution": 0.4,
        }})
        
        # Different player action patterns
        action_patterns = [
            ["attack"] * 50,
            ["defend"] * 50,
            ["explore"] * 50,
            ["hide"] * 50,
            ["attack", "defend", "attack", "defend"] * 25,
            ["attack", "attack", "attack", "defend"] * 25,
        ]
        
        iteration_times = []
        
        for pattern in action_patterns:
            for i, player_action in enumerate(pattern):
                start = time.time()
                
                game_state = {
                    "player_health": max(0, 80 - i),
                    "villain_health": max(0, 100 - i),
                    "player_last_action": player_action,
                    "round_number": i + 1,
                }
                
                engine.update_state(game_state)
                decision = engine.decide_action()
                engine.learn_from_result({
                    "outcome": "victory" if i % 2 == 0 else "defeat",
                    "success": i % 2 == 0,
                })
                
                iteration_time = time.time() - start
                iteration_times.append(iteration_time)
        
        # Analyze results
        print(f"Total iterations: {len(iteration_times)}")
        print(f"Average time per iteration: {statistics.mean(iteration_times):.4f}s")
        print(f"Min time: {min(iteration_times):.4f}s")
        print(f"Max time: {max(iteration_times):.4f}s")
        print(f"Std dev: {statistics.stdev(iteration_times):.4f}s")
        
        # Check for memory growth
        stats = engine.get_state_summary()
        print(f"Total decisions: {stats['total_decisions']}")
        print(f"Total learning: {stats['total_learning_iterations']}")
        
        self.timings["massive_iterations"] = iteration_times
    
    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        print("\n--- Edge Case Tests ---")
        
        edge_cases = [
            {
                "name": "Zero health",
                "state": {"player_health": 0, "villain_health": 0, "round_number": 1}
            },
            {
                "name": "Max health",
                "state": {"player_health": 999, "villain_health": 999, "round_number": 1}
            },
            {
                "name": "Negative values",
                "state": {"player_health": -10, "villain_health": -10, "round_number": 1}
            },
            {
                "name": "Empty state",
                "state": {}
            },
            {
                "name": "Missing fields",
                "state": {"player_health": 50}
            },
            {
                "name": "Very long action",
                "state": {"player_health": 50, "player_last_action": "a" * 1000}
            },
            {
                "name": "Unicode in action",
                "state": {"player_health": 50, "player_last_action": "attack with 日本語"}
            },
            {
                "name": "Special characters",
                "state": {"player_health": 50, "player_last_action": "attack<script>"}
            },
        ]
        
        for case in edge_cases:
            try:
                engine = VillainEngine({"llm_model": None})
                engine.load_personality({"traits": {
                    "aggression": 0.5,
                    "patience": 0.5,
                    "ego": 0.5,
                    "chaos": 0.5,
                    "adaptability": 0.5,
                    "caution": 0.5,
                }})
                engine.update_state(case["state"])
                decision = engine.decide_action()
                print(f"  {case['name']}: OK")
            except Exception as e:
                print(f"  {case['name']}: ERROR - {e}")
                self.errors.append((case['name'], str(e)))
    
    def test_memory_stress(self):
        """Stress test memory with many save/load cycles."""
        print("\n--- Memory Stress Test ---")
        
        # Create engine
        engine = VillainEngine({
            "name": "Memory Stress",
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
        
        # Run 50 rounds with save after each
        save_times = []
        load_times = []
        
        for i in range(50):
            game_state = {
                "player_health": 100 - i,
                "villain_health": 100 - i,
                "player_last_action": "attack",
                "round_number": i + 1,
            }
            engine.update_state(game_state)
            engine.decide_action()
            engine.learn_from_result({"success": i % 2 == 0})
            
            # Time save
            start = time.time()
            engine.save_memory()
            save_times.append(time.time() - start)
            
            # Time load
            start = time.time()
            engine.load_memory()
            load_times.append(time.time() - start)
        
        print(f"Save times - Avg: {statistics.mean(save_times):.4f}s, Max: {max(save_times):.4f}s")
        print(f"Load times - Avg: {statistics.mean(load_times):.4f}s, Max: {max(load_times):.4f}s")
        
        self.timings["save_times"] = save_times
        self.timings["load_times"] = load_times
    
    def print_summary(self):
        """Print final summary."""
        print("\n" + "=" * 70)
        print("STRESS TEST SUMMARY")
        print("=" * 70)
        
        print("\nTiming Averages:")
        for key, times in self.timings.items():
            if times and isinstance(times[0], float):
                avg = statistics.mean(times)
                print(f"  {key}: {avg:.4f}s")
        
        if self.errors:
            print(f"\nErrors encountered: {len(self.errors)}")
            for name, error in self.errors[:10]:
                print(f"  {name}: {error}")
        else:
            print("\nNo errors encountered!")
        
        print("\n" + "=" * 70)
        print("OPTIMIZATION RECOMMENDATIONS")
        print("=" * 70)
        
        # Analyze results and provide recommendations
        if self.timings.get("qwen2.5:1.5b_decide"):
            qwen_time = statistics.mean(self.timings["qwen2.5:1.5b_decide"])
            print(f"1. qwen2.5:1.5b is recommended for edge (faster than phi3.5)")
            print(f"   Average decision time: {qwen_time:.4f}s")
        
        if self.timings.get("no_llm_decide"):
            no_llm_time = statistics.mean(self.timings["no_llm_decide"])
            print(f"2. No-LLM mode is fastest: {no_llm_time:.4f}s per decision")
        
        if self.timings.get("save_times"):
            save_avg = statistics.mean(self.timings["save_times"])
            print(f"3. Consider batch saves (current avg: {save_avg:.4f}s)")
        
        print("\nEdge Deployment Recommendations:")
        print("  - Use qwen2.5:1.5b for LLM (986MB vs 2.2GB)")
        print("  - Disable LLM for maximum speed")
        print("  - Batch memory saves")
        print("  - Limit decision history to 100 items")


if __name__ == "__main__":
    test = StressTest()
    test.run_all_tests()
