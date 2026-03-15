"""
Perception system - converts raw game state into structured observations.

This module provides game-agnostic perception capabilities for analyzing
player behavior, health states, and environment features.
"""

from typing import Dict, Any, List


class PerceptionSystem:
    """
    Converts raw game state into structured observations for decision making.
    
    Game-agnostic perception system that analyzes player behavior patterns,
    health states, environment features, and game phase to extract relevant
    features for decision making.
    
    Configuration allows customization of thresholds for different games.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the perception system with optional configuration.
        
        Args:
            config: Optional configuration dictionary with custom thresholds.
                   Supported keys:
                   - health_low_threshold: Value below which health is "low" (default: 30)
                   - health_high_threshold: Value above which health is "high" (default: 70)
                   - round_early_threshold: Round number considered "early" (default: 3)
                   - round_late_threshold: Round number considered "late" (default: 15)
                   - aggressive_actions: List of actions considered aggressive (default: ["attack", "fight", "aggressive"])
                   - trap_awareness_weights: Weights for trap awareness calculation
        """
        self.config = config or {}
        
        self.health_low_threshold = self.config.get("health_low_threshold", 30)
        self.health_high_threshold = self.config.get("health_high_threshold", 70)
        self.round_early_threshold = self.config.get("round_early_threshold", 3)
        self.round_late_threshold = self.config.get("round_late_threshold", 15)
        
        self.aggressive_actions = self.config.get(
            "aggressive_actions", 
            ["attack", "fight", "aggressive", "strike", "assault"]
        )
        
        self.trap_awareness_weights = self.config.get(
            "trap_awareness_weights",
            {
                "avoids_traps": 0.4,
                "uses_cover": 0.3,
                "checks_environment": 0.3
            }
        )
        
        self._behavior_history: List[Dict[str, Any]] = []
    
    def perceive(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main perception method - converts raw game state to structured observations.
        
        Args:
            game_state: Dictionary containing game state information.
                       Expected keys:
                       - player_health: int (0-100)
                       - villain_health: int (0-100)
                       - player_last_action: str
                       - environment_objects: List[str]
                       - round_number: int
        
        Returns:
            Dictionary of structured observations including:
            - player_is_aggressive: bool
            - player_health_low: bool
            - player_health_high: bool
            - villain_health_low: bool
            - environment_has_traps: bool
            - player_pattern_aggressive: bool
            - player_trap_awareness: float
            - round_early: bool
            - round_late: bool
        """
        observations = {}
        
        health_states = self.analyze_health_states(game_state)
        observations.update(health_states)
        
        environment = self.analyze_environment(game_state)
        observations.update(environment)
        
        current_action = game_state.get("player_last_action", "")
        observations["player_is_aggressive"] = self._is_aggressive_action(current_action)
        
        behavior_analysis = self.analyze_player_behavior(game_state, self._behavior_history)
        observations.update(behavior_analysis)
        
        round_num = game_state.get("round_number", 1)
        observations["round_early"] = round_num <= self.round_early_threshold
        observations["round_late"] = round_num >= self.round_late_threshold
        
        self._update_history(game_state)
        
        return observations
    
    def analyze_player_behavior(
        self, 
        game_state: Dict[str, Any], 
        history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze player behavior patterns from current state and history.
        
        Args:
            game_state: Current game state dictionary.
            history: List of previous game states for pattern analysis.
        
        Returns:
            Dictionary containing:
            - player_pattern_aggressive: bool - True if player shows aggressive patterns
            - player_trap_awareness: float - 0.0 to 1.0 awareness score
        """
        analysis: Dict[str, Any] = {}
        
        all_states = history + [game_state] if history else [game_state]
        
        aggressive_count = 0
        total_actions = len(all_states)
        
        for state in all_states:
            action = state.get("player_last_action", "")
            if self._is_aggressive_action(action):
                aggressive_count += 1
        
        if total_actions > 0:
            aggression_ratio = aggressive_count / total_actions
            analysis["player_pattern_aggressive"] = aggression_ratio >= 0.6
        else:
            current_action = game_state.get("player_last_action", "")
            analysis["player_pattern_aggressive"] = self._is_aggressive_action(current_action)
        
        analysis["player_trap_awareness"] = self._calculate_trap_awareness(
            game_state, 
            all_states
        )
        
        return analysis
    
    def analyze_health_states(self, game_state: Dict[str, Any]) -> Dict[str, bool]:
        """
        Analyze health-related observations from game state.
        
        Args:
            game_state: Dictionary containing health information.
                       Expected keys:
                       - player_health: int (0-100)
                       - villain_health: int (0-100)
        
        Returns:
            Dictionary containing:
            - player_health_low: bool
            - player_health_high: bool
            - villain_health_low: bool
        """
        player_health = game_state.get("player_health", 100)
        villain_health = game_state.get("villain_health", 100)
        
        return {
            "player_health_low": player_health <= self.health_low_threshold,
            "player_health_high": player_health >= self.health_high_threshold,
            "villain_health_low": villain_health <= self.health_low_threshold,
        }
    
    def analyze_environment(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze environment-related observations from game state.
        
        Args:
            game_state: Dictionary containing environment information.
                       Expected keys:
                       - environment_objects: List[str]
        
        Returns:
            Dictionary containing:
            - environment_has_traps: bool
            - environment_has_cover: bool
            - environment_object_count: int
        """
        environment_objects = game_state.get("environment_objects", [])
        
        object_lower = [obj.lower() for obj in environment_objects]
        
        return {
            "environment_has_traps": "trap" in object_lower or "traps" in object_lower,
            "environment_has_cover": "cover" in object_lower or "obstacle" in object_lower,
            "environment_object_count": len(environment_objects),
        }
    
    def _is_aggressive_action(self, action: str) -> bool:
        """Check if an action is considered aggressive."""
        if not action:
            return False
        action_lower = action.lower()
        return any(
            aggressive in action_lower 
            for aggressive in self.aggressive_actions
        )
    
    def _calculate_trap_awareness(
        self, 
        current_state: Dict[str, Any],
        history: List[Dict[str, Any]]
    ) -> float:
        """Calculate player trap awareness based on behavior patterns."""
        if not history:
            return 0.3
        
        avoids_traps = 0
        uses_cover = 0
        checks_environment = 0
        total = len(history)
        
        for state in history:
            action = state.get("player_last_action", "").lower()
            env_objects = state.get("environment_objects", [])
            env_lower = [obj.lower() for obj in env_objects]
            
            if "trap" in env_lower and "avoid" in action:
                avoids_traps += 1
            
            if "cover" in env_lower and "use" in action:
                uses_cover += 1
            
            if env_objects and len(env_objects) > 0:
                checks_environment += 1
        
        awareness = (
            (avoids_traps / total) * self.trap_awareness_weights["avoids_traps"] +
            (uses_cover / total) * self.trap_awareness_weights["uses_cover"] +
            (checks_environment / total) * self.trap_awareness_weights["checks_environment"]
        )
        
        return min(max(awareness, 0.0), 1.0)
    
    def _update_history(self, game_state: Dict[str, Any]) -> None:
        """Update internal behavior history with current state."""
        self._behavior_history.append(game_state)
        
        max_history = 20
        if len(self._behavior_history) > max_history:
            self._behavior_history = self._behavior_history[-max_history:]
    
    def reset_history(self) -> None:
        """Clear the behavior history."""
        self._behavior_history = []
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get the current behavior history."""
        return self._behavior_history.copy()
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update perception system configuration."""
        self.config.update(config)
        
        if "health_low_threshold" in config:
            self.health_low_threshold = config["health_low_threshold"]
        if "health_high_threshold" in config:
            self.health_high_threshold = config["health_high_threshold"]
        if "round_early_threshold" in config:
            self.round_early_threshold = config["round_early_threshold"]
        if "round_late_threshold" in config:
            self.round_late_threshold = config["round_late_threshold"]
        if "aggressive_actions" in config:
            self.aggressive_actions = config["aggressive_actions"]
        if "trap_awareness_weights" in config:
            self.trap_awareness_weights = config["trap_awareness_weights"]
