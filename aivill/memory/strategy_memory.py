"""
Strategy memory module - stores learned strategies and their effectiveness.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class StrategyMemory:
    """
    Stores successful strategies and their outcomes for future reference.
    
    Attributes:
        strategies: Dictionary of strategy records
        success_history: History of strategy outcomes
        adaptation_count: Number of strategy adaptations made
    """
    
    def __init__(self):
        self.strategies: Dict[str, Dict[str, Any]] = {}
        self.success_history: List[Dict[str, Any]] = []
        self.adaptation_count = 0
        self.total_uses = 0
    
    def store_strategy(
        self,
        strategy_id: str,
        strategy_data: Dict[str, Any],
        effectiveness: float = 0.5
    ) -> None:
        """Store a strategy with its effectiveness rating."""
        if strategy_id not in self.strategies:
            self.strategies[strategy_id] = {
                "strategy_id": strategy_id,
                "data": strategy_data,
                "effectiveness": effectiveness,
                "use_count": 0,
                "success_count": 0,
                "failure_count": 0,
                "first_used": datetime.now().isoformat(),
                "last_used": datetime.now().isoformat(),
                "effectiveness_history": []
            }
        
        self.strategies[strategy_id]["use_count"] += 1
        self.strategies[strategy_id]["last_used"] = datetime.now().isoformat()
        self.total_uses += 1
    
    def record_outcome(
        self,
        strategy_id: str,
        success: bool,
        outcome_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record the outcome of a strategy application."""
        if strategy_id not in self.strategies:
            return
        
        strategy = self.strategies[strategy_id]
        
        if success:
            strategy["success_count"] += 1
        else:
            strategy["failure_count"] += 1
        
        use_count = strategy["use_count"]
        if use_count > 0:
            new_effectiveness = strategy["success_count"] / use_count
            strategy["effectiveness"] = new_effectiveness
            strategy["effectiveness_history"].append({
                "effectiveness": new_effectiveness,
                "timestamp": datetime.now().isoformat()
            })
            
            if len(strategy["effectiveness_history"]) > 50:
                strategy["effectiveness_history"] = strategy["effectiveness_history"][-50:]
        
        self.success_history.append({
            "strategy_id": strategy_id,
            "success": success,
            "outcome_data": outcome_data or {},
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.success_history) > 500:
            self.success_history = self.success_history[-500:]
    
    def get_best_strategies(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get the top performing strategies."""
        sorted_strategies = sorted(
            self.strategies.values(),
            key=lambda s: s.get("effectiveness", 0),
            reverse=True
        )
        return sorted_strategies[:limit]
    
    def get_worst_strategies(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Get the worst performing strategies for analysis."""
        sorted_strategies = sorted(
            self.strategies.values(),
            key=lambda s: s.get("effectiveness", 1)
        )
        return sorted_strategies[:limit]
    
    def get_strategy(self, strategy_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific strategy by ID."""
        return self.strategies.get(strategy_id)
    
    def increment_adaptation(self) -> None:
        """Increment the adaptation counter."""
        self.adaptation_count += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        total_strategies = len(self.strategies)
        avg_effectiveness = sum(
            s.get("effectiveness", 0) for s in self.strategies.values()
        ) / max(total_strategies, 1)
        
        return {
            "total_strategies": total_strategies,
            "total_uses": self.total_uses,
            "adaptation_count": self.adaptation_count,
            "average_effectiveness": avg_effectiveness,
            "success_history_length": len(self.success_history)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "strategies": self.strategies,
            "success_history": self.success_history,
            "adaptation_count": self.adaptation_count,
            "total_uses": self.total_uses
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StrategyMemory":
        """Deserialize from dictionary."""
        memory = cls()
        memory.strategies = data.get("strategies", {})
        memory.success_history = data.get("success_history", [])
        memory.adaptation_count = data.get("adaptation_count", 0)
        memory.total_uses = data.get("total_uses", 0)
        return memory
