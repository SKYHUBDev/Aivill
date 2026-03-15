"""
Pattern learning - identifies patterns in player behavior.
"""

from typing import Dict, Any, List, Optional
from collections import defaultdict, Counter


class PatternLearning:
    """
    Identifies and learns patterns from player behavior.
    
    Analyzes decision history to detect recurring patterns,
    strategic tendencies, and predictable behaviors.
    """
    
    def __init__(self, memory_manager=None):
        self.memory_manager = memory_manager
        self.detected_patterns: Dict[str, Any] = {}
        self.pattern_confidences: Dict[str, float] = {}
        self.observation_count = 0
    
    def learn_from_interaction(
        self,
        interaction: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Learn patterns from an interaction.
        
        Args:
            interaction: The interaction data
            
        Returns:
            Detected patterns
        """
        self.observation_count += 1
        
        patterns_found = {}
        
        if self.memory_manager:
            player_id = interaction.get("player_id", "default")
            player = self.memory_manager.get_player_profile(player_id)
            
            if player:
                action_type = interaction.get("action_type", "unknown")
                player.preferred_strategies.append(action_type)
                
                if len(player.preferred_strategies) > 20:
                    player.preferred_strategies = player.preferred_strategies[-20:]
                
                patterns_found["preferred_strategy"] = player.get_strategy_preference()
                
                risk_observed = interaction.get("risk_level", 0.5)
                player.update_risk_tolerance(risk_observed)
                
                trust_change = interaction.get("trust_change", 0.0)
                if trust_change != 0:
                    player.update_trust(trust_change)
        
        return patterns_found
    
    def detect_temporal_patterns(
        self,
        events: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Detect temporal patterns in events."""
        if not events:
            return {}
        
        action_types = [e.get("action_type", "unknown") for e in events]
        action_counter = Counter(action_types)
        
        patterns = {
            "most_common_action": action_counter.most_common(1)[0][0] if action_counter else None,
            "action_diversity": len(action_counter),
            "total_observations": len(events)
        }
        
        return patterns
    
    def detect_response_patterns(
        self,
        events: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Detect how player responds to different situations."""
        response_map = defaultdict(list)
        
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]
            
            situation = current.get("situation", "unknown")
            response = next_event.get("action_type", "unknown")
            
            response_map[situation].append(response)
        
        patterns = {}
        for situation, responses in response_map.items():
            most_common = Counter(responses).most_common(1)[0]
            patterns[situation] = {
                "likely_response": most_common[0],
                "confidence": most_common[1] / len(responses) if responses else 0
            }
        
        return patterns
    
    def update_pattern_confidence(
        self,
        pattern_id: str,
        confirmed: bool
    ) -> None:
        """Update confidence in a detected pattern."""
        current = self.pattern_confidences.get(pattern_id, 0.5)
        
        if confirmed:
            new_confidence = current + (1 - current) * 0.2
        else:
            new_confidence = current * 0.8
        
        self.pattern_confidences[pattern_id] = new_confidence
    
    def get_pattern(self, pattern_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific pattern."""
        return self.detected_patterns.get(pattern_id)
    
    def get_all_patterns(self) -> Dict[str, Any]:
        """Get all detected patterns."""
        return {
            "patterns": self.detected_patterns,
            "confidences": self.pattern_confidences,
            "observation_count": self.observation_count
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pattern learning statistics."""
        return {
            "patterns_detected": len(self.detected_patterns),
            "observations": self.observation_count,
            "avg_confidence": sum(self.pattern_confidences.values()) / 
                             max(len(self.pattern_confidences), 1)
        }
