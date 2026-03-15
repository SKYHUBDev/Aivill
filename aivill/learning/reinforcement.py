"""
Reinforcement learning module.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from collections import defaultdict
import random


class ReinforcementLearning:
    """
    Implements reinforcement learning for strategy optimization.
    
    Uses Q-learning inspired approach to evaluate and improve
    action selection based on rewards and outcomes.
    """
    
    def __init__(
        self,
        learning_rate: float = 0.1,
        discount_factor: float = 0.9,
        exploration_rate: float = 0.2
    ):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        
        self.q_values: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.action_history: list[Dict[str, Any]] = []
        self.total_reward = 0.0
    
    def process_outcome(
        self,
        action: str,
        outcome: str,
        reward: float
    ) -> Dict[str, Any]:
        """
        Process an action outcome and update Q-values.
        
        Args:
            action: The action that was taken
            outcome: The outcome of the action
            reward: The reward received
            
        Returns:
            Update information
        """
        state = self._get_state_from_outcome(outcome)
        
        current_q = self.q_values[state][action]
        
        max_future_q = max(self.q_values[state].values()) if self.q_values[state] else 0.0
        
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_future_q - current_q
        )
        
        self.q_values[state][action] = new_q
        
        self.total_reward += reward
        
        self.action_history.append({
            "action": action,
            "state": state,
            "reward": reward,
            "q_value": new_q,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.action_history) > 500:
            self.action_history = self.action_history[-500:]
        
        return {
            "action": action,
            "state": state,
            "old_q": current_q,
            "new_q": new_q,
            "reward": reward
        }
    
    def _get_state_from_outcome(self, outcome: str) -> str:
        """Map outcome to a state representation."""
        outcome_states = {
            "victory": "winning",
            "defeat": "losing",
            "partial": "neutral",
            "unknown": "uncertain"
        }
        return outcome_states.get(outcome, "uncertain")
    
    def select_action(
        self,
        available_actions: list[str],
        state: str = "current"
    ) -> str:
        """
        Select an action using epsilon-greedy strategy.
        
        Args:
            available_actions: List of possible actions
            state: Current state
            
        Returns:
            Selected action
        """
        if not available_actions:
            return "none"
        
        if random.random() < self.exploration_rate:
            return random.choice(available_actions)
        
        state_q_values = self.q_values.get(state, {})
        
        if not state_q_values:
            return random.choice(available_actions)
        
        best_actions = [
            action for action, q in state_q_values.items()
            if action in available_actions and q == max(state_q_values.values())
        ]
        
        if not best_actions:
            return random.choice(available_actions)
        
        return random.choice(best_actions)
    
    def get_action_value(self, action: str, state: str = "current") -> float:
        """Get the Q-value for an action in a state."""
        return self.q_values.get(state, {}).get(action, 0.0)
    
    def get_best_action(
        self,
        available_actions: list[str],
        state: str = "current"
    ) -> Optional[str]:
        """Get the best action for a state."""
        if not available_actions:
            return None
        
        state_q_values = self.q_values.get(state, {})
        
        if not state_q_values:
            return available_actions[0]
        
        best_action = None
        best_value = float('-inf')
        
        for action in available_actions:
            value = state_q_values.get(action, 0.0)
            if value > best_value:
                best_value = value
                best_action = action
        
        return best_action or available_actions[0]
    
    def decay_exploration(self, decay_rate: float = 0.95) -> None:
        """Decay the exploration rate."""
        self.exploration_rate = max(0.05, self.exploration_rate * decay_rate)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get reinforcement learning statistics."""
        all_q_values = []
        for state_actions in self.q_values.values():
            all_q_values.extend(state_actions.values())
        
        return {
            "states_visited": len(self.q_values),
            "actions_explored": sum(len(actions) for actions in self.q_values.values()),
            "total_reward": self.total_reward,
            "avg_q_value": sum(all_q_values) / max(len(all_q_values), 1),
            "exploration_rate": self.exploration_rate,
            "history_length": len(self.action_history)
        }
    
    def get_q_table(self) -> Dict[str, Dict[str, float]]:
        """Get the full Q-table."""
        return dict(self.q_values)
