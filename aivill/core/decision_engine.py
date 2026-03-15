"""
Decision engine - processes inputs and makes strategic decisions.
"""

import random
from typing import Dict, Any, Optional, List
from datetime import datetime


class DecisionEngine:
    """
    Processes game state and makes strategic decisions.
    
    Integrates personality, memory, and strategy to select
    appropriate actions in different situations.
    """
    
    def __init__(
        self,
        personality_engine=None,
        memory_manager=None,
        strategy_engine=None,
        learning_engine=None
    ):
        self.personality_engine = personality_engine
        self.memory_manager = memory_manager
        self.strategy_engine = strategy_engine
        self.learning_engine = learning_engine
        
        self.decision_history: List[Dict[str, Any]] = []
        self.decision_count = 0
    
    def make_decision(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Make a decision based on current context.
        
        Args:
            context: Current game state and situation
            
        Returns:
            Decision with action and reasoning
        """
        self.decision_count += 1
        
        available_actions = context.get("available_actions", self._get_default_actions())
        
        if self.strategy_engine:
            strategy = self.strategy_engine.select_strategy(context)
            self.strategy_engine.increment_execution()
        else:
            strategy = {"strategy_id": "default", "template": {"name": "Default"}}
        
        action = self._select_action_from_strategy(
            available_actions,
            strategy,
            context
        )
        
        decision = {
            "decision_id": self.decision_count,
            "action": action,
            "strategy": strategy.get("template", {}).get("name", "unknown"),
            "strategy_id": strategy.get("strategy_id", "unknown"),
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        
        self.decision_history.append(decision)
        
        if len(self.decision_history) > 100:
            self.decision_history = self.decision_history[-100:]
        
        return decision
    
    def _get_default_actions(self) -> List[str]:
        """Get default available actions."""
        return [
            "direct_attack",
            "scheming",
            "opportunistic",
            "defensive",
            "intimidating",
            "negotiating",
            "chaotic"
        ]
    
    def _select_action_from_strategy(
        self,
        available_actions: List[str],
        strategy: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Select an action based on strategy and context."""
        if not self.personality_engine:
            return random.choice(available_actions) if available_actions else "wait"
        
        traits = self.personality_engine.get_traits()
        
        strategy_name = strategy.get("template", {}).get("name", "")
        
        action_weights = self._calculate_action_weights(
            strategy_name,
            traits,
            context
        )
        
        filtered_actions = [
            a for a in available_actions 
            if a in action_weights
        ]
        
        if not filtered_actions:
            return available_actions[0] if available_actions else "wait"
        
        weights = [action_weights.get(a, 0.1) for a in filtered_actions]
        total = sum(weights)
        weights = [w / total for w in weights]
        
        return random.choices(filtered_actions, weights=weights)[0]
    
    def _calculate_action_weights(
        self,
        strategy_name: str,
        traits: Dict[str, float],
        context: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate weights for available actions."""
        weights = {}
        
        aggression = traits.get("aggression", 0.5)
        patience = traits.get("patience", 0.5)
        ego = traits.get("ego", 0.5)
        chaos = traits.get("chaos", 0.5)
        caution = traits.get("caution", 0.5)
        
        weights["direct_attack"] = aggression * 0.8 + (1 - caution) * 0.2
        weights["scheming"] = patience * 0.9 + caution * 0.1
        weights["opportunistic"] = (1 - caution) * 0.6 + chaos * 0.3
        weights["defensive"] = caution * 0.9 + (1 - aggression) * 0.1
        weights["intimidating"] = aggression * 0.7 + ego * 0.3
        weights["negotiating"] = patience * 0.5 + (1 - aggression) * 0.3 + caution * 0.2
        weights["chaotic"] = chaos * 0.9 + (1 - patience) * 0.1
        
        return weights
    
    def process_outcome(
        self,
        decision: Dict[str, Any],
        outcome: Dict[str, Any]
    ) -> None:
        """Process the outcome of a decision for learning."""
        if outcome is None:
            outcome_dict = {"type": "unknown", "success": False, "reward": 0.0}
        elif isinstance(outcome, str):
            outcome_dict = {"type": outcome, "success": True, "reward": 1.0}
        else:
            outcome_dict = outcome

        if self.learning_engine:
            self.learning_engine.process_interaction({
                "action": decision.get("action"),
                "outcome": outcome_dict.get("type", "unknown"),
                "success": outcome_dict.get("success", False),
                "reward": outcome_dict.get("reward", 0.0)
            })
        
        if self.strategy_engine and outcome_dict:
            self.strategy_engine.record_outcome(
                decision.get("strategy_id", "unknown"),
                outcome_dict.get("success", False),
                outcome_dict
            )
    
    def get_decision_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent decision history."""
        return self.decision_history[-limit:]
    
    def get_decision_stats(self) -> Dict[str, Any]:
        """Get decision statistics."""
        return {
            "total_decisions": self.decision_count,
            "history_length": len(self.decision_history)
        }
