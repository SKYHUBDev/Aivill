"""
Villain Leaderboard System

Allows recording and ranking of villain strategies.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class VillainLeaderboard:
    """Manages the villain strategy leaderboard."""
    
    def __init__(self, data_dir: str = "leaderboard"):
        self.data_dir = Path(data_dir)
        self.data_file = self.data_dir / "leaderboard.json"
        self.entries: List[Dict[str, Any]] = []
        self._load()
    
    def _load(self) -> None:
        """Load leaderboard from file."""
        if self.data_file.exists():
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    self.entries = data.get("entries", [])
            except (json.JSONDecodeError, IOError):
                self.entries = []
        else:
            self.entries = []
    
    def _save(self) -> None:
        """Save leaderboard to file."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "entries": self.entries,
            "updated": datetime.now().isoformat()
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def add_entry(
        self,
        villain_name: str,
        strategy: str,
        win_rate: float,
        rounds_tested: int,
        personality: Optional[Dict[str, float]] = None,
        description: str = ""
    ) -> None:
        """Add a new villain entry to the leaderboard."""
        entry = {
            "villain_name": villain_name,
            "strategy": strategy,
            "win_rate": round(win_rate, 3),
            "rounds_tested": rounds_tested,
            "rank": 0,  # Will be calculated
            "personality": personality or {},
            "description": description,
            "submitted": datetime.now().isoformat()
        }
        
        # Check if updating existing entry
        for i, existing in enumerate(self.entries):
            if existing["villain_name"] == villain_name:
                self.entries[i] = entry
                break
        else:
            self.entries.append(entry)
        
        # Recalculate rankings
        self._update_rankings()
        self._save()
    
    def _update_rankings(self) -> None:
        """Update rankings based on win rate."""
        # Sort by win rate descending
        sorted_entries = sorted(self.entries, key=lambda x: x["win_rate"], reverse=True)
        
        # Assign ranks
        for rank, entry in enumerate(sorted_entries, 1):
            entry["rank"] = rank
        
        self.entries = sorted_entries
    
    def get_top(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get top N villains."""
        return self.entries[:n]
    
    def get_rank(self, villain_name: str) -> Optional[int]:
        """Get rank of a specific villain."""
        for entry in self.entries:
            if entry["villain_name"] == villain_name:
                return entry["rank"]
        return None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all entries."""
        return self.entries
    
    def clear(self) -> None:
        """Clear all entries."""
        self.entries = []
        self._save()


# Default leaderboard with example entries
DEFAULT_ENTRIES = [
    {
        "villain_name": "trap_master_v2",
        "strategy": "adaptive_trap_strategy",
        "win_rate": 0.91,
        "rounds_tested": 100,
        "personality": {
            "aggression": 0.3,
            "patience": 0.9,
            "ego": 0.5,
            "chaos": 0.2,
            "adaptability": 0.8,
            "caution": 0.7
        },
        "description": "Patient trap-based strategy that adapts to player movement patterns"
    },
    {
        "villain_name": "chaos_overlord",
        "strategy": "chaos_manipulation",
        "win_rate": 0.86,
        "rounds_tested": 100,
        "personality": {
            "aggression": 0.9,
            "patience": 0.3,
            "ego": 0.8,
            "chaos": 0.95,
            "adaptability": 0.6,
            "caution": 0.2
        },
        "description": "Unpredictable villain that thrives on chaos and aggression"
    },
    {
        "villain_name": "mind_reader",
        "strategy": "predictive_counter",
        "win_rate": 0.82,
        "rounds_tested": 100,
        "personality": {
            "aggression": 0.5,
            "patience": 0.8,
            "ego": 0.6,
            "chaos": 0.1,
            "adaptability": 0.95,
            "caution": 0.5
        },
        "description": "Highly adaptive strategy that learns and predicts player patterns"
    },
    {
        "villain_name": "aggressive_berserker",
        "strategy": "rush_strategy",
        "win_rate": 0.78,
        "rounds_tested": 100,
        "personality": {
            "aggression": 0.95,
            "patience": 0.2,
            "ego": 0.9,
            "chaos": 0.3,
            "adaptability": 0.4,
            "caution": 0.1
        },
        "description": "Overwhelming aggressive force that doesn't give players time to think"
    },
    {
        "villain_name": "defensive_turtle",
        "strategy": "fortress_strategy",
        "win_rate": 0.65,
        "rounds_tested": 100,
        "personality": {
            "aggression": 0.2,
            "patience": 0.9,
            "ego": 0.3,
            "chaos": 0.1,
            "adaptability": 0.5,
            "caution": 0.95
        },
        "description": "Nearly impenetrable defense that waits for player mistakes"
    }
]


def init_leaderboard():
    """Initialize leaderboard with default entries."""
    leaderboard = VillainLeaderboard()
    if not leaderboard.entries:
        for entry in DEFAULT_ENTRIES:
            leaderboard.add_entry(**entry)
    return leaderboard
