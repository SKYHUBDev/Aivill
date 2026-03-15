"""
Utility helpers for AiVill package.
"""

from typing import Any, Dict, List
import random


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(max_val, value))


def weighted_choice(choices: List[str], weights: List[float]) -> str:
    """Select a random choice based on weights."""
    if not choices or not weights:
        return ""
    total = sum(weights)
    if total == 0:
        return random.choice(choices)
    normalized = [w / total for w in weights]
    return random.choices(choices, weights=normalized)[0]


def format_traits(traits: Dict[str, float]) -> str:
    """Format traits dictionary as a readable string."""
    return ", ".join(f"{k}: {v:.2f}" for k, v in traits.items())


def calculate_reward(success: bool, base_reward: float = 1.0) -> float:
    """Calculate reward based on success/failure."""
    return base_reward if success else -base_reward


def merge_dicts(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge two dictionaries."""
    result = base.copy()
    for key, value in update.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result
