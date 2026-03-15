"""
Learning engine - coordinates all learning systems.
"""

from typing import Dict, Any

from aivill.learning.pattern_learning import PatternLearning
from aivill.learning.reinforcement import ReinforcementLearning


class LearningEngine:
    """
    Coordinates all learning systems including pattern recognition
    and reinforcement learning.
    
    Manages the overall learning process and integrates insights
    from different learning subsystems.
    """
    
    def __init__(
        self,
        memory_manager=None,
        personality_engine=None,
        strategy_engine=None
    ):
        self.memory_manager = memory_manager
        self.personality_engine = personality_engine
        self.strategy_engine = strategy_engine
        
        self.pattern_learning = PatternLearning(memory_manager)
        self.reinforcement = ReinforcementLearning()
        
        self.learning_events: list[Dict[str, Any]] = []
        self.total_learning_iterations = 0
    
    def process_interaction(
        self,
        interaction: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process an interaction and learn from it.
        
        Args:
            interaction: The interaction data to learn from
            
        Returns:
            Learning insights from the interaction
        """
        self.total_learning_iterations += 1
        
        insights = {}
        
        pattern_insights = self.pattern_learning.learn_from_interaction(interaction)
        insights["patterns"] = pattern_insights
        
        reinforcement_insights = self.reinforcement.process_outcome(
            interaction.get("action", "unknown"),
            interaction.get("outcome", "unknown"),
            interaction.get("reward", 0.0)
        )
        insights["reinforcement"] = reinforcement_insights
        
        if self.personality_engine and interaction.get("outcome"):
            self._update_personality_from_learning(interaction)
        
        from datetime import datetime
        self.learning_events.append({
            "interaction": interaction,
            "insights": insights,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.learning_events) > 200:
            self.learning_events = self.learning_events[-200:]
        
        return insights
    
    def _update_personality_from_learning(self, interaction: Dict[str, Any]) -> None:
        """Update personality based on learning outcomes."""
        outcome = interaction.get("outcome", "")
        success = interaction.get("success", False)
        
        if outcome == "victory" or outcome == "defeat":
            outcome_type = outcome
            magnitude = interaction.get("magnitude", 0.1)
            self.personality_engine.apply_outcome_to_personality(
                outcome_type, success, magnitude
            )
        
        elif outcome == "player_trust" or outcome == "player_distrust":
            if "trust" in outcome:
                self.personality_engine.apply_outcome_to_personality(
                    "trust_gained" if success else "betrayal",
                    success,
                    0.1
                )
        
        elif outcome == "risk_taken":
            self.personality_engine.apply_outcome_to_personality(
                "risk_taken",
                success,
                0.15
            )
    
    def adapt_strategy(
        self,
        current_strategy: Dict[str, Any],
        outcome: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Adapt strategy based on outcome.
        
        Args:
            current_strategy: Current strategy being used
            outcome: Result of the strategy execution
            
        Returns:
            Adapted strategy
        """
        if not self.strategy_engine:
            return current_strategy
        
        success = outcome.get("success", False)
        
        self.strategy_engine.record_outcome(
            current_strategy.get("strategy_id", "unknown"),
            success,
            outcome
        )
        
        if not success:
            adaptation_rate = 0.3
            if self.personality_engine:
                traits = self.personality_engine.get_traits()
                adaptation_rate = traits.get("adaptability", 0.5) * 0.5
            
            return self.strategy_engine.mutate_strategy(
                current_strategy,
                mutation_type=None,
                strength=adaptation_rate
            )
        
        return current_strategy
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics."""
        return {
            "total_iterations": self.total_learning_iterations,
            "learning_events": len(self.learning_events),
            "pattern_recognition": self.pattern_learning.get_stats(),
            "reinforcement": self.reinforcement.get_stats()
        }
    
    def get_recent_insights(self, count: int = 5) -> list[Dict[str, Any]]:
        """Get recent learning insights."""
        return self.learning_events[-count:]
