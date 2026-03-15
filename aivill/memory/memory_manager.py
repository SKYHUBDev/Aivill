"""
Memory manager - coordinates all memory systems with JSON persistence.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from aivill.memory.player_profile import PlayerProfile
from aivill.memory.strategy_memory import StrategyMemory
from aivill.memory.short_term_memory import ShortTermMemory


class MemoryManager:
    """
    Coordinates all memory systems with JSON persistence.
    
    Manages long-term memory (player profiles, strategies) and
    short-term memory (recent events, context).
    """
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.memory_file = self.data_dir / "aivill_memory.json"
        self.profiles_file = self.data_dir / "aivill_players.json"
        self.strategies_file = self.data_dir / "aivill_strategies.json"
        
        self.player_profiles: Dict[str, PlayerProfile] = {}
        self.strategy_memory = StrategyMemory()
        self.short_term_memory = ShortTermMemory()
        
        self._load_all()
    
    def _load_all(self) -> None:
        """Load all memory data from JSON files."""
        self._load_player_profiles()
        self._load_strategy_memory()
    
    def _load_player_profiles(self) -> None:
        """Load player profiles from JSON."""
        try:
            if self.profiles_file.exists():
                with open(self.profiles_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for player_id, profile_data in data.items():
                        self.player_profiles[player_id] = PlayerProfile.from_dict(profile_data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load player profiles: {e}")
            self.player_profiles = {}
    
    def _save_player_profiles(self) -> None:
        """Save player profiles to JSON."""
        try:
            data = {
                pid: profile.to_dict() 
                for pid, profile in self.player_profiles.items()
            }
            with open(self.profiles_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save player profiles: {e}")
    
    def _load_strategy_memory(self) -> None:
        """Load strategy memory from JSON."""
        try:
            if self.strategies_file.exists():
                with open(self.strategies_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.strategy_memory = StrategyMemory.from_dict(data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load strategy memory: {e}")
            self.strategy_memory = StrategyMemory()
    
    def _save_strategy_memory(self) -> None:
        """Save strategy memory to JSON."""
        try:
            with open(self.strategies_file, "w", encoding="utf-8") as f:
                json.dump(self.strategy_memory.to_dict(), f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save strategy memory: {e}")
    
    def get_player_profile(self, player_id: str) -> Optional[PlayerProfile]:
        """Get a player profile by ID."""
        return self.player_profiles.get(player_id)
    
    def get_or_create_player_profile(self, player_id: str, name: str = "Unknown") -> PlayerProfile:
        """Get existing profile or create new one."""
        if player_id not in self.player_profiles:
            self.player_profiles[player_id] = PlayerProfile(player_id, name)
            self._save_player_profiles()
        return self.player_profiles[player_id]
    
    def update_player_profile(self, player_id: str, **kwargs) -> None:
        """Update a player profile."""
        profile = self.get_or_create_player_profile(player_id)
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        self._save_player_profiles()
    
    def get_short_term(self) -> ShortTermMemory:
        """Get the short-term memory instance."""
        return self.short_term_memory
    
    def get_strategy(self) -> StrategyMemory:
        """Get the strategy memory instance."""
        return self.strategy_memory
    
    def save_all(self) -> None:
        """Save all memory data to disk."""
        self._save_player_profiles()
        self._save_strategy_memory()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics."""
        return {
            "player_profiles": len(self.player_profiles),
            "short_term_events": self.short_term_memory.get_event_count(),
            **self.strategy_memory.get_stats()
        }
    
    def log_event(self, event: Dict[str, Any]) -> None:
        """Log an event to short-term memory."""
        self.short_term_memory.add_event(event)
    
    def get_all_profiles(self) -> Dict[str, PlayerProfile]:
        """Get all player profiles."""
        return self.player_profiles

    def save_engine_state(self, state: Dict[str, Any]) -> None:
        """Save engine state (decisions, learning iterations, etc)."""
        state_file = self.data_dir / "aivill_engine_state.json"
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)

    def load_engine_state(self) -> Dict[str, Any]:
        """Load engine state from disk."""
        state_file = self.data_dir / "aivill_engine_state.json"
        if state_file.exists():
            with open(state_file, "r") as f:
                return json.load(f)
        return {}
