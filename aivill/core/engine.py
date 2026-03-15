"""
VillainEngine - Main AI controller for the AiVill package.
"""

from typing import Dict, Any, Optional
from pathlib import Path

from aivill.memory.memory_manager import MemoryManager
from aivill.personality.personality_engine import PersonalityEngine
from aivill.strategy.strategy_engine import StrategyEngine
from aivill.learning.learning_engine import LearningEngine
from aivill.core.decision_engine import DecisionEngine
from aivill.logging.event_logger import EventLogger
from aivill.core.perception import PerceptionSystem
from aivill.llm.ollama_client import OllamaClient


class VillainEngine:
    """
    The main villain AI engine that orchestrates all systems.
    
    Integrates memory, personality, strategy, learning, perception, and
    decision-making into a cohesive AI entity.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = self.config.get("name", "The Villain")
        
        data_dir = Path(self.config.get("data_dir", "data"))
        log_dir = Path(self.config.get("log_dir", "logs"))
        
        self.memory = MemoryManager(data_dir)
        self.personality = PersonalityEngine()
        self.event_logger = EventLogger(log_dir / "aivill_events.jsonl")
        self.perception = PerceptionSystem()
        
        self.strategy = StrategyEngine(
            personality_engine=self.personality,
            memory_manager=self.memory
        )
        
        self.learning = LearningEngine(
            memory_manager=self.memory,
            personality_engine=self.personality,
            strategy_engine=self.strategy
        )
        
        self.decision = DecisionEngine(
            personality_engine=self.personality,
            memory_manager=self.memory,
            strategy_engine=self.strategy,
            learning_engine=self.learning
        )
        
        self.total_decisions = 0
        self.total_learning_iterations = 0
        self.current_game_state: Dict[str, Any] = {}
        self._last_decision: Dict[str, Any] = {}
        
        llm_model = self.config.get("llm_model", "phi3.5")
        self.ollama = OllamaClient(model=llm_model)
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the engine with configuration."""
        self.config.update(config)
        if "name" in config:
            self.name = config["name"]
    
    def get_llm_suggestion(self, prompt: str) -> Optional[str]:
        """Get a suggestion from the LLM."""
        if self.ollama and self.ollama.is_connected():
            return self.ollama.generate(prompt)
        return None
    
    @property
    def llm_available(self) -> bool:
        """Check if LLM is available."""
        return hasattr(self, 'ollama') and self.ollama and self.ollama.is_connected()
    
    def load_personality(self, profile: Dict[str, Any]) -> None:
        """Load a personality profile."""
        if "traits" in profile:
            for trait, value in profile["traits"].items():
                self.personality.set_trait(trait, value, "loaded_profile")
    
    def update_state(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the game state and return perceived observations.
        
        Args:
            game_state: Current game state dictionary
            
        Returns:
            Perceived observations for decision making
        """
        self.current_game_state = game_state
        observations = self.perception.perceive(game_state)
        
        self.event_logger.log_game_event("state_update", {
            "game_state": game_state,
            "observations": observations
        })
        
        return observations
    
    def decide_action(self) -> Dict[str, Any]:
        """
        Make a decision based on the current game state.
        
        Returns:
            Decision dictionary with action and reasoning
        """
        context = {
            "game_state": self.current_game_state,
            "available_actions": self.current_game_state.get(
                "available_actions",
                ["direct_attack", "scheming", "opportunistic", "defensive", "intimidating", "negotiating", "chaotic"]
            ),
            "player_id": self.current_game_state.get("player_id", "default")
        }
        
        self.event_logger.log_villain_decision({
            "context": context
        })
        
        decision = self.decision.make_decision(context)
        
        self._last_decision = decision
        self.total_decisions += 1
        
        self.event_logger.log_outcome(
            action=decision.get("action", "unknown"),
            outcome="pending",
            success=False
        )
        
        return decision
    
    def learn_from_result(self, result: Dict[str, Any]) -> None:
        """
        Learn from the outcome of a decision.
        
        Args:
            result: Result dictionary containing success, reward, etc.
                   Can be in two formats:
                   1. With "decision" key: {"decision": {...}, "outcome": {...}}
                   2. Without "decision" key: {"damage_dealt": 15, "outcome": "advantage", "success": True, ...}
        """
        if "decision" in result:
            decision = result.get("decision", {})
            outcome = result.get("outcome", {})
        else:
            decision = self._last_decision
            outcome = result
        
        if isinstance(outcome, str):
            outcome = {"type": outcome, "success": result.get("success", True)}
        
        self.decision.process_outcome(decision, outcome)
        
        if outcome.get("success") is not None:
            outcome_type = "victory" if outcome.get("success") else "defeat"
            magnitude = abs(outcome.get("reward", 0.1))
            self.personality.apply_outcome_to_personality(
                outcome_type,
                outcome.get("success", False),
                min(magnitude, 0.3)
            )
        
        self.event_logger.log_outcome(
            action=decision.get("action", "unknown"),
            outcome=outcome.get("type", "unknown"),
            success=outcome.get("success", False),
            details=result
        )
        
        self.total_learning_iterations += 1
    
    def save_memory(self) -> None:
        """Save all memory data to disk."""
        if self.memory:
            self.memory.save_all()
            engine_state = {
                "total_decisions": self.total_decisions,
                "total_learning_iterations": self.total_learning_iterations
            }
            self.memory.save_engine_state(engine_state)
    
    def load_memory(self) -> None:
        """Reload memory from disk."""
        if self.memory:
            self.memory._load_all()
            engine_state = self.memory.load_engine_state()
            self.total_decisions = engine_state.get("total_decisions", 0)
            self.total_learning_iterations = engine_state.get("total_learning_iterations", 0)
    
    def get_player_profile(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Get a player profile by ID."""
        if self.memory:
            profile = self.memory.get_player_profile(player_id)
            if profile:
                return profile.to_dict()
        return None
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get a summary of the engine's current state."""
        return {
            "name": self.name,
            "total_decisions": self.total_decisions,
            "total_learning_iterations": self.total_learning_iterations,
            "personality": self.personality.get_traits(),
            "strategy": self.strategy.get_strategy_info() if self.strategy else {},
            "memory": self.memory.get_stats() if self.memory else {},
            "llm_available": self.llm_available
        }
    
    def adapt_personality(self, trait: str, delta: float, reason: str = "") -> None:
        """Adapt a personality trait."""
        old_traits = self.personality.get_traits()
        self.personality.modify_trait(trait, delta, reason)
        new_traits = self.personality.get_traits()
        
        self.event_logger.log_personality_change(
            trait,
            old_traits.get(trait, 0),
            new_traits.get(trait, 0),
            reason
        )
    
    def get_personality_traits(self) -> Dict[str, float]:
        """Get current personality traits."""
        return self.personality.get_traits()

    def get_personality(self) -> Dict[str, float]:
        """Get personality traits."""
        if hasattr(self, 'personality') and self.personality:
            return self.personality.get_traits()
        return {}
