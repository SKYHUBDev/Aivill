"""
Player profile module - tracks information about players.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class PlayerProfile:
    """
    Stores comprehensive information about a player for strategic adaptation.
    
    Attributes:
        player_id: Unique identifier for the player
        name: Player's display name
        decision_history: List of player's past decisions
        interaction_count: Number of interactions with this player
        trust_level: Current trust level (-1.0 to 1.0)
        risk_tolerance: Player's observed risk tolerance
        preferred_strategies: Player's preferred strategic approaches
        learned_patterns: Patterns learned from player behavior
    """
    
    def __init__(self, player_id: str, name: str = "Unknown"):
        self.player_id = player_id
        self.name = name
        self.decision_history: List[Dict[str, Any]] = []
        self.interaction_count = 0
        self.trust_level = 0.0
        self.risk_tolerance = 0.5
        self.preferred_strategies: List[str] = []
        self.learned_patterns: Dict[str, Any] = {}
        self.created_at = datetime.now().isoformat()
        self.last_interaction = datetime.now().isoformat()
    
    def add_decision(self, decision: Dict[str, Any]) -> None:
        """Record a player decision in their history."""
        self.decision_history.append({
            **decision,
            "timestamp": datetime.now().isoformat()
        })
        self.interaction_count += 1
        self.last_interaction = datetime.now().isoformat()
        
        if len(self.decision_history) > 100:
            self.decision_history = self.decision_history[-100:]
    
    def update_trust(self, delta: float) -> None:
        """Update trust level based on interactions."""
        self.trust_level = max(-1.0, min(1.0, self.trust_level + delta))
    
    def update_risk_tolerance(self, observed: float) -> None:
        """Update risk tolerance based on observed behavior."""
        self.risk_tolerance = 0.7 * self.risk_tolerance + 0.3 * observed
    
    def add_pattern(self, pattern_name: str, pattern_data: Dict[str, Any]) -> None:
        """Add a learned pattern from player behavior."""
        if pattern_name in self.learned_patterns:
            self.learned_patterns[pattern_name]["count"] += 1
            self.learned_patterns[pattern_name]["last_seen"] = datetime.now().isoformat()
        else:
            self.learned_patterns[pattern_name] = {
                "count": 1,
                "first_seen": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "data": pattern_data
            }
    
    def get_strategy_preference(self) -> str:
        """Get the player's most preferred strategy."""
        if not self.preferred_strategies:
            return "balanced"
        return max(set(self.preferred_strategies), 
                   key=self.preferred_strategies.count)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "player_id": self.player_id,
            "name": self.name,
            "decision_history": self.decision_history,
            "interaction_count": self.interaction_count,
            "trust_level": self.trust_level,
            "risk_tolerance": self.risk_tolerance,
            "preferred_strategies": self.preferred_strategies,
            "learned_patterns": self.learned_patterns,
            "created_at": self.created_at,
            "last_interaction": self.last_interaction
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlayerProfile":
        """Create PlayerProfile from dictionary."""
        profile = cls(data.get("player_id", "unknown"), data.get("name", "Unknown"))
        profile.decision_history = data.get("decision_history", [])
        profile.interaction_count = data.get("interaction_count", 0)
        profile.trust_level = data.get("trust_level", 0.0)
        profile.risk_tolerance = data.get("risk_tolerance", 0.5)
        profile.preferred_strategies = data.get("preferred_strategies", [])
        profile.learned_patterns = data.get("learned_patterns", {})
        profile.created_at = data.get("created_at", datetime.now().isoformat())
        profile.last_interaction = data.get("last_interaction", datetime.now().isoformat())
        return profile
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the player profile."""
        return {
            "player_id": self.player_id,
            "name": self.name,
            "interactions": self.interaction_count,
            "trust": self.trust_level,
            "risk_tolerance": self.risk_tolerance,
            "preferred_strategy": self.get_strategy_preference()
        }
