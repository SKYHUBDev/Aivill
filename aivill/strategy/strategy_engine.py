"""
Strategy engine - generates and manages villain strategies.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import random

from aivill.strategy.mutation import MutationEngine


class StrategyEngine:
    """
    Generates and manages villain strategies with learning capabilities.
    
    Handles strategy selection, generation, and adaptation based on
    personality traits and historical success.
    """
    
    STRATEGY_TEMPLATES = {
        "direct_attack": {
            "name": "Direct Attack",
            "aggression_weight": 0.9,
            "chaos_weight": 0.3,
            "description": "Open confrontation with target"
        },
        "scheming": {
            "name": "Scheming",
            "patience_weight": 0.9,
            "caution_weight": 0.7,
            "description": "Long-term planning and manipulation"
        },
        "opportunistic": {
            "name": "Opportunistic",
            "adaptability_weight": 0.8,
            "chaos_weight": 0.6,
            "description": "Exploiting unexpected opportunities"
        },
        "defensive": {
            "name": "Defensive",
            "caution_weight": 0.9,
            "patience_weight": 0.6,
            "description": "Protecting current assets and position"
        },
        "intimidating": {
            "name": "Intimidating",
            "aggression_weight": 0.8,
            "ego_weight": 0.7,
            "description": "Using fear and power displays"
        },
        "negotiating": {
            "name": "Negotiating",
            "patience_weight": 0.7,
            "caution_weight": 0.5,
            "description": "Diplomatic approach with leverage"
        },
        "chaotic": {
            "name": "Chaotic",
            "chaos_weight": 0.95,
            "aggression_weight": 0.6,
            "description": "Unpredictable and erratic actions"
        }
    }
    
    def __init__(self, personality_engine=None, memory_manager=None):
        self.personality_engine = personality_engine
        self.memory_manager = memory_manager
        self.mutation_engine = MutationEngine()
        
        self.current_strategy: Optional[Dict[str, Any]] = None
        self.strategy_history: List[Dict[str, Any]] = []
        self.strategy_count = 0
    
    def select_strategy(
        self,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Select the most appropriate strategy based on personality and context.
        
        Args:
            context: Current game context and situation
            
        Returns:
            Selected strategy dictionary
        """
        if self.personality_engine is None:
            return self._get_default_strategy()
        
        traits = self.personality_engine.get_traits()
        
        scored_strategies = []
        for strategy_id, template in self.STRATEGY_TEMPLATES.items():
            score = self._calculate_strategy_score(template, traits)
            
            if self.memory_manager:
                strategy_mem = self.memory_manager.get_strategy()
                stored = strategy_mem.get_strategy(strategy_id)
                if stored:
                    score *= (0.5 + stored.get("effectiveness", 0.5))
            
            scored_strategies.append((strategy_id, template, score))
        
        scored_strategies.sort(key=lambda x: x[2], reverse=True)
        
        top_strategy_id, top_template, top_score = scored_strategies[0]
        
        if random.random() < traits.get("chaos", 0.3) and len(scored_strategies) > 1:
            _, top_template, _ = random.choice(scored_strategies[1:])
        
        self.current_strategy = {
            "strategy_id": top_strategy_id,
            "template": top_template,
            "score": top_score,
            "context": context or {},
            "selected_at": datetime.now().isoformat(),
            "execution_count": 0
        }
        
        self.strategy_count += 1
        
        return self.current_strategy
    
    def _calculate_strategy_score(
        self,
        template: Dict[str, Any],
        traits: Dict[str, float]
    ) -> float:
        """Calculate a strategy's suitability score based on personality."""
        score = 0.5
        
        score += template.get("aggression_weight", 0) * traits.get("aggression", 0.5)
        score += template.get("patience_weight", 0) * traits.get("patience", 0.5)
        score += template.get("ego_weight", 0) * traits.get("ego", 0.5)
        score += template.get("chaos_weight", 0) * traits.get("chaos", 0.5)
        score += template.get("adaptability_weight", 0) * traits.get("adaptability", 0.5)
        score += template.get("caution_weight", 0) * traits.get("caution", 0.5)
        
        return score / 3.0
    
    def _get_default_strategy(self) -> Dict[str, Any]:
        """Get a default strategy when no personality engine is available."""
        return {
            "strategy_id": "balanced",
            "template": {"name": "Balanced", "description": "Standard approach"},
            "score": 0.5,
            "context": {},
            "selected_at": datetime.now().isoformat(),
            "execution_count": 0
        }
    
    def mutate_strategy(
        self,
        strategy: Dict[str, Any],
        mutation_type: Optional[str] = None,
        strength: float = 0.1
    ) -> Dict[str, Any]:
        """
        Apply mutations to a strategy based on outcomes.
        
        Args:
            strategy: The strategy to mutate
            mutation_type: Optional specific mutation type
            
        Returns:
            Mutated strategy
        """
        if self.personality_engine:
            traits = self.personality_engine.get_traits()
        else:
            traits = {"chaos": 0.3, "adaptability": 0.5}
        
        mutation_strength = traits.get("adaptability", 0.5) * 0.3
        
        mutated = self.mutation_engine.mutate(strategy, mutation_type, mutation_strength)
        
        self.strategy_history.append({
            "original": strategy,
            "mutated": mutated,
            "timestamp": datetime.now().isoformat()
        })
        
        return mutated
    
    def record_outcome(
        self,
        strategy_id: str,
        success: bool,
        outcome_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record the outcome of a strategy for learning."""
        if self.memory_manager:
            strategy_mem = self.memory_manager.get_strategy()
            strategy_mem.store_strategy(strategy_id, {})
            strategy_mem.record_outcome(strategy_id, success, outcome_data)
            
            if not success:
                self.mutate_strategy({"strategy_id": strategy_id})
                strategy_mem.increment_adaptation()
    
    def get_current_strategy(self) -> Optional[Dict[str, Any]]:
        """Get the currently active strategy."""
        return self.current_strategy
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """Get information about the current strategy."""
        if not self.current_strategy:
            return {"status": "no_active_strategy"}
        
        return {
            "current": self.current_strategy.get("template", {}).get("name", "Unknown"),
            "score": self.current_strategy.get("score", 0),
            "executions": self.current_strategy.get("execution_count", 0),
            "total_strategies": self.strategy_count
        }
    
    def increment_execution(self) -> None:
        """Increment the execution counter for current strategy."""
        if self.current_strategy:
            self.current_strategy["execution_count"] += 1
