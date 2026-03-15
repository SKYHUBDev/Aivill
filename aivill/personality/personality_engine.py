"""
Personality engine - manages villain personality traits and modifications.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class PersonalityEngine:
    """
    Manages the villain's personality with trait modifiers.
    
    Personality Traits:
        - aggression: Tendency toward hostile actions (0.0-1.0)
        - patience: Willingness to wait for opportunities (0.0-1.0)
        - ego: Self-importance and pride (0.0-1.0)
        - chaos: Appreciation for disorder and unpredictability (0.0-1.0)
        - adaptability: Ability to adjust strategies (0.0-1.0)
        - caution: Risk-aversion level (0.0-1.0)
    
    Traits are modified through interactions and learning.
    """
    
    DEFAULT_TRAITS = {
        "aggression": 0.6,
        "patience": 0.5,
        "ego": 0.7,
        "chaos": 0.4,
        "adaptability": 0.5,
        "caution": 0.4
    }
    
    TRAIT_BOUNDS = {
        "aggression": (0.0, 1.0),
        "patience": (0.0, 1.0),
        "ego": (0.0, 1.0),
        "chaos": (0.0, 1.0),
        "adaptability": (0.0, 1.0),
        "caution": (0.0, 1.0)
    }
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path
        self.traits: Dict[str, float] = self.DEFAULT_TRAITS.copy()
        self.trait_history: list[Dict[str, Any]] = []
        self.major_events: list[Dict[str, Any]] = []
        
        if config_path and config_path.exists():
            self._load_config()
    
    def _load_config(self) -> None:
        """Load personality configuration from JSON."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                loaded_traits = config.get("traits", {})
                for trait, value in loaded_traits.items():
                    if trait in self.traits:
                        self.traits[trait] = self._bound_trait(trait, value)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load personality config: {e}")
    
    def _bound_trait(self, trait: str, value: float) -> float:
        """Bound a trait value to its valid range."""
        min_val, max_val = self.TRAIT_BOUNDS.get(trait, (0.0, 1.0))
        return max(min_val, min(max_val, value))
    
    def get_traits(self) -> Dict[str, float]:
        """Get current personality traits."""
        return self.traits.copy()
    
    def get_trait(self, trait: str) -> float:
        """Get a specific trait value."""
        return self.traits.get(trait, 0.5)
    
    def modify_trait(self, trait: str, delta: float, reason: str = "") -> None:
        """
        Modify a personality trait by a delta value.
        
        Args:
            trait: The trait to modify
            delta: The amount to change (positive or negative)
            reason: Optional reason for the modification
        """
        if trait not in self.traits:
            return
        
        old_value = self.traits[trait]
        new_value = self._bound_trait(trait, old_value + delta)
        self.traits[trait] = new_value
        
        self.trait_history.append({
            "trait": trait,
            "old_value": old_value,
            "new_value": new_value,
            "delta": delta,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.trait_history) > 100:
            self.trait_history = self.trait_history[-100:]
    
    def set_trait(self, trait: str, value: float, reason: str = "") -> None:
        """Set a trait to a specific value."""
        if trait not in self.traits:
            return
        
        old_value = self.traits[trait]
        new_value = self._bound_trait(trait, value)
        self.traits[trait] = new_value
        
        self.trait_history.append({
            "trait": trait,
            "old_value": old_value,
            "new_value": new_value,
            "delta": new_value - old_value,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
    
    def record_major_event(self, event: Dict[str, Any]) -> None:
        """Record a major event that affects personality."""
        self.major_events.append({
            **event,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.major_events) > 50:
            self.major_events = self.major_events[-50:]
    
    def apply_outcome_to_personality(
        self,
        outcome_type: str,
        success: bool,
        magnitude: float = 0.1
    ) -> None:
        """
        Apply an outcome to modify personality traits.
        
        Args:
            outcome_type: Type of outcome (victory, defeat, betrayal, trust, etc.)
            success: Whether the outcome was positive for the villain
            magnitude: How strongly to modify traits (0.0-1.0)
        """
        magnitude = max(0.01, min(0.3, magnitude))
        
        if outcome_type == "victory":
            self.modify_trait("ego", magnitude * (1 if success else -1), f"outcome:{outcome_type}")
            self.modify_trait("aggression", magnitude * 0.5 if success else -magnitude * 0.5, f"outcome:{outcome_type}")
        
        elif outcome_type == "defeat":
            self.modify_trait("caution", magnitude if success else -magnitude, f"outcome:{outcome_type}")
            self.modify_trait("aggression", -magnitude * 0.5 if success else magnitude, f"outcome:{outcome_type}")
            self.modify_trait("patience", magnitude * 0.5, f"outcome:{outcome_type}")
        
        elif outcome_type == "betrayal":
            self.modify_trait("caution", magnitude, f"outcome:{outcome_type}")
            self.modify_trait("aggression", magnitude * 0.5, f"outcome:{outcome_type}")
        
        elif outcome_type == "trust_gained":
            self.modify_trait("ego", -magnitude * 0.3, f"outcome:{outcome_type}")
            self.modify_trait("caution", -magnitude * 0.2, f"outcome:{outcome_type}")
        
        elif outcome_type == "patience_tested":
            if not success:
                self.modify_trait("patience", -magnitude, f"outcome:{outcome_type}")
                self.modify_trait("chaos", magnitude * 0.5, f"outcome:{outcome_type}")
            else:
                self.modify_trait("patience", magnitude * 0.5, f"outcome:{outcome_type}")
        
        elif outcome_type == "risk_taken":
            if success:
                self.modify_trait("chaos", magnitude, f"outcome:{outcome_type}")
                self.modify_trait("ego", magnitude * 0.5, f"outcome:{outcome_type}")
            else:
                self.modify_trait("caution", magnitude, f"outcome:{outcome_type}")
                self.modify_trait("chaos", -magnitude * 0.5, f"outcome:{outcome_type}")
        
        self.record_major_event({
            "outcome_type": outcome_type,
            "success": success,
            "magnitude": magnitude,
            "current_traits": self.traits.copy()
        })
    
    def get_personality_summary(self) -> Dict[str, Any]:
        """Get a summary of the current personality."""
        return {
            "traits": self.traits.copy(),
            "trait_history_count": len(self.trait_history),
            "major_events_count": len(self.major_events)
        }
    
    def get_dominant_trait(self) -> str:
        """Get the most dominant trait."""
        return max(self.traits, key=self.traits.get)
    
    def get_behavior_modifiers(self) -> Dict[str, float]:
        """
        Get behavioral modifiers based on personality for decision making.
        
        Returns:
            Dictionary of behavior multipliers based on personality
        """
        return {
            "aggression_multiplier": 1.0 + (self.traits["aggression"] - 0.5),
            "patience_multiplier": 1.0 + (self.traits["patience"] - 0.5) * 2,
            "caution_multiplier": 1.0 + (self.traits["caution"] - 0.5) * 2,
            "chaos_acceptance": self.traits["chaos"],
            "adaptation_rate": 0.5 + self.traits["adaptability"] * 0.5,
            "ego_defense_threshold": 0.3 + self.traits["ego"] * 0.4
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "traits": self.traits,
            "trait_history": self.trait_history,
            "major_events": self.major_events
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PersonalityEngine":
        """Deserialize from dictionary."""
        engine = cls()
        engine.traits = data.get("traits", cls.DEFAULT_TRAITS.copy())
        engine.trait_history = data.get("trait_history", [])
        engine.major_events = data.get("major_events", [])
        return engine
