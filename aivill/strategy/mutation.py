"""
Mutation engine - handles strategy mutation and variation.
"""

import random
from typing import Dict, Any, Optional, List


class MutationEngine:
    """
    Handles mutation of strategies for evolutionary learning.
    
    Applies various mutation types to create strategy variations
    that can be tested for effectiveness.
    """
    
    MUTATION_TYPES = [
        "parameter_adjust",
        "tactic_swap",
        "risk_modulation",
        "temporal_shift",
        "target_change",
        "method_alteration"
    ]
    
    def __init__(self, base_mutation_rate: float = 0.1):
        self.base_mutation_rate = base_mutation_rate
        self.mutation_history: List[Dict[str, Any]] = []
    
    def mutate(
        self,
        strategy: Dict[str, Any],
        mutation_type: Optional[str] = None,
        strength: float = 0.1
    ) -> Dict[str, Any]:
        """
        Apply mutation to a strategy.
        
        Args:
            strategy: The strategy to mutate
            mutation_type: Specific mutation to apply (random if None)
            strength: Intensity of mutation (0.0-1.0)
            
        Returns:
            Mutated strategy
        """
        if mutation_type is None:
            mutation_type = random.choice(self.MUTATION_TYPES)
        
        mutated = strategy.copy()
        
        if "template" in strategy:
            mutated["template"] = strategy["template"].copy()
        
        if mutation_type == "parameter_adjust":
            mutated = self._mutate_parameters(mutated, strength)
        elif mutation_type == "tactic_swap":
            mutated = self._swap_tactics(mutated, strength)
        elif mutation_type == "risk_modulation":
            mutated = self._modulate_risk(mutated, strength)
        elif mutation_type == "temporal_shift":
            mutated = self._shift_timing(mutated, strength)
        elif mutation_type == "target_change":
            mutated = self._change_target(mutated, strength)
        elif mutation_type == "method_alteration":
            mutated = self._alter_method(mutated, strength)
        
        mutated["mutated"] = True
        mutated["mutation_type"] = mutation_type
        mutated["mutation_strength"] = strength
        
        return mutated
    
    def _mutate_parameters(
        self,
        strategy: Dict[str, Any],
        strength: float
    ) -> Dict[str, Any]:
        """Adjust strategy parameters."""
        template = strategy.get("template", {})
        
        for key in ["aggression_weight", "patience_weight", "chaos_weight", 
                    "caution_weight", "ego_weight", "adaptability_weight"]:
            if key in template:
                delta = (random.random() - 0.5) * strength
                template[key] = max(0, min(1, template[key] + delta))
        
        strategy["template"] = template
        return strategy
    
    def _swap_tactics(self, strategy: Dict[str, Any], strength: float) -> Dict[str, Any]:
        """Swap tactical approach."""
        if random.random() < strength:
            template = strategy.get("template", {})
            current_name = template.get("name", "")
            
            alternative_approaches = {
                "Direct Attack": ["Intimidating", "Chaotic"],
                "Scheming": ["Negotiating", "Defensive"],
                "Opportunistic": ["Direct Attack", "Chaotic"],
                "Defensive": ["Scheming", "Intimidating"],
                "Intimidating": ["Direct Attack", "Chaotic"],
                "Negotiating": ["Scheming", "Defensive"],
                "Chaotic": ["Opportunistic", "Direct Attack"]
            }
            
            if current_name in alternative_approaches:
                template["name"] = random.choice(alternative_approaches[current_name])
                strategy["template"] = template
        
        return strategy
    
    def _modulate_risk(
        self,
        strategy: Dict[str, Any],
        strength: float
    ) -> Dict[str, Any]:
        """Modulate the risk level of a strategy."""
        template = strategy.get("template", {})
        
        if "risk_level" not in template:
            template["risk_level"] = 0.5
        
        template["risk_level"] += (random.random() - 0.5) * strength
        template["risk_level"] = max(0, min(1, template["risk_level"]))
        
        strategy["template"] = template
        return strategy
    
    def _shift_timing(
        self,
        strategy: Dict[str, Any],
        strength: float
    ) -> Dict[str, Any]:
        """Shift the timing characteristics of a strategy."""
        template = strategy.get("template", {})
        
        if "timing" not in template:
            template["timing"] = "moderate"
        
        timing_options = ["immediate", "gradual", "delayed", "burst", "sustained"]
        if random.random() < strength:
            current = template.get("timing", "moderate")
            if current in timing_options:
                timing_options.remove(current)
            template["timing"] = random.choice(timing_options)
        
        strategy["template"] = template
        return strategy
    
    def _change_target(
        self,
        strategy: Dict[str, Any],
        strength: float
    ) -> Dict[str, Any]:
        """Change the target/focus of the strategy."""
        template = strategy.get("template", {})
        
        if random.random() < strength:
            target_options = ["player", "resources", "reputation", "allies", "territory"]
            template["target"] = random.choice(target_options)
        
        strategy["template"] = template
        return strategy
    
    def _alter_method(
        self,
        strategy: Dict[str, Any],
        strength: float
    ) -> Dict[str, Any]:
        """Alter the method of execution."""
        template = strategy.get("template", {})
        
        method_variations = {
            "force": ["negotiation", "deception", "manipulation"],
            "negotiation": ["force", "deception", "alliance"],
            "deception": ["force", "negotiation", "manipulation"],
            "manipulation": ["deception", "alliance", "force"],
            "alliance": ["manipulation", "negotiation", "deception"]
        }
        
        current_method = template.get("method", "force")
        if current_method in method_variations and random.random() < strength:
            template["method"] = random.choice(method_variations[current_method])
        
        strategy["template"] = template
        return strategy
    
    def get_mutation_history(self) -> List[Dict[str, Any]]:
        """Get the history of mutations."""
        return self.mutation_history
