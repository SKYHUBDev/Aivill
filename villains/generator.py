"""
Villain Personality Generator

Generates unique villain personalities with optional LLM descriptions.
"""

import random
from typing import Dict, Optional, Any


class PersonalityGenerator:
    """Generates unique villain personalities."""
    
    # Archetype templates
    ARCHETYPES = {
        "the_calculating_tyrant": {
            "traits": {"aggression": 0.6, "patience": 0.85, "ego": 0.7, "chaos": 0.1, "adaptability": 0.8, "caution": 0.6},
            "description": "A patient strategist who studies the player's weaknesses before striking."
        },
        "the_chaos_overlord": {
            "traits": {"aggression": 0.9, "patience": 0.2, "ego": 0.9, "chaos": 0.95, "adaptability": 0.4, "caution": 0.1},
            "description": "An unpredictable force of destruction who revels in mayhem."
        },
        "the_mind_reader": {
            "traits": {"aggression": 0.4, "patience": 0.9, "ego": 0.5, "chaos": 0.05, "adaptability": 0.95, "caution": 0.5},
            "description": "A master psychologist who predicts and counters every move."
        },
        "the_aggressive_berserker": {
            "traits": {"aggression": 0.95, "patience": 0.1, "ego": 0.85, "chaos": 0.4, "adaptability": 0.3, "caution": 0.05},
            "description": "A relentless warrior who knows only attack, never retreat."
        },
        "the_defensive_turtle": {
            "traits": {"aggression": 0.15, "patience": 0.95, "ego": 0.3, "chaos": 0.05, "adaptability": 0.5, "caution": 0.95},
            "description": "An impenetrable fortress that waits for opponents to make mistakes."
        },
        "the_trickster": {
            "traits": {"aggression": 0.4, "patience": 0.6, "ego": 0.7, "chaos": 0.7, "adaptability": 0.8, "caution": 0.3},
            "description": "A deceptive mastermind who misleads and outsmarts opponents."
        },
        "the_sadist": {
            "traits": {"aggression": 0.7, "patience": 0.7, "ego": 0.8, "chaos": 0.5, "adaptability": 0.6, "caution": 0.3},
            "description": "A cruel antagonist who enjoys toying with victims before finishing them."
        },
        "the_mercenary": {
            "traits": {"aggression": 0.5, "patience": 0.5, "ego": 0.4, "chaos": 0.3, "adaptability": 0.9, "caution": 0.6},
            "description": "A practical fighter who adapts tactics based on what works best."
        },
        "the_egomaniac": {
            "traits": {"aggression": 0.6, "patience": 0.3, "ego": 0.98, "chaos": 0.2, "adaptability": 0.4, "caution": 0.4},
            "description": "An arrogant villain who underestimates opponents due to overwhelming confidence."
        },
        "the_shadow": {
            "traits": {"aggression": 0.3, "patience": 0.8, "ego": 0.5, "chaos": 0.2, "adaptability": 0.9, "caution": 0.8},
            "description": "A stealthy hunter who observes, learns, and strikes when least expected."
        }
    }
    
    # Name components
    PREFIXES = ["Dark", "Shadow", "Iron", "Blood", "Storm", "Frost", "Void", "Crimson", "Winter", " Eternal"]
    TITLES = ["Lord", "King", "Master", "Overlord", "Tyrant", "Emperor", "Warlord", "Prince", "Duke", "Knight"]
    NOUNS = ["Shadow", "Flame", "Storm", "Night", "Death", "Doom", "Chaos", "Fury", "Rage", "Despair"]
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
    
    def generate_random(self) -> Dict[str, Any]:
        """Generate a completely random personality."""
        traits = {
            "aggression": random.random(),
            "patience": random.random(),
            "ego": random.random(),
            "chaos": random.random(),
            "adaptability": random.random(),
            "caution": random.random()
        }
        
        name = self._generate_name()
        
        return {
            "name": name,
            "traits": traits,
            "description": self._describe_from_traits(traits)
        }
    
    def generate_from_archetype(self, archetype: str) -> Dict[str, Any]:
        """Generate personality from a predefined archetype."""
        if archetype not in self.ARCHETYPES:
            archetype = random.choice(list(self.ARCHETYPES.keys()))
        
        template = self.ARCHETYPES[archetype]
        
        # Add some variation
        traits = {}
        for trait, value in template["traits"].items():
            variation = random.uniform(-0.1, 0.1)
            traits[trait] = max(0, min(1, value + variation))
        
        return {
            "name": self._generate_name(),
            "archetype": archetype,
            "traits": traits,
            "description": template["description"]
        }
    
    def generate_balanced(self) -> Dict[str, Any]:
        """Generate a balanced personality."""
        traits = {
            "aggression": 0.5 + random.uniform(-0.2, 0.2),
            "patience": 0.5 + random.uniform(-0.2, 0.2),
            "ego": 0.5 + random.uniform(-0.2, 0.2),
            "chaos": 0.2 + random.uniform(-0.1, 0.1),
            "adaptability": 0.6 + random.uniform(-0.2, 0.2),
            "caution": 0.5 + random.uniform(-0.2, 0.2)
        }
        
        return {
            "name": self._generate_name(),
            "traits": traits,
            "description": self._describe_from_traits(traits)
        }
    
    def generate_extreme(self) -> Dict[str, Any]:
        """Generate a personality with extreme traits."""
        # Pick one trait to be very high, one to be very low
        traits = {
            "aggression": random.choice([random.uniform(0.8, 1.0), random.uniform(0.0, 0.2)]),
            "patience": random.choice([random.uniform(0.8, 1.0), random.uniform(0.0, 0.2)]),
            "ego": random.choice([random.uniform(0.8, 1.0), random.uniform(0.0, 0.2)]),
            "chaos": random.choice([random.uniform(0.8, 1.0), random.uniform(0.0, 0.2)]),
            "adaptability": random.uniform(0.3, 0.8),
            "caution": random.choice([random.uniform(0.8, 1.0), random.uniform(0.0, 0.2)])
        }
        
        return {
            "name": self._generate_name(),
            "traits": traits,
            "description": self._describe_from_traits(traits)
        }
    
    def generate_with_llm(self) -> Optional[Dict[str, Any]]:
        """Generate personality with LLM description."""
        base = self.generate_random()
        
        if self.llm_client and self.llm_client.is_connected():
            prompt = f"""Generate a villain personality description for these traits:
{base['traits']}

Create a short, menacing description (1-2 sentences)."""
            description = self.llm_client.generate(prompt)
            if description:
                base["description"] = description
        
        return base
    
    def _generate_name(self) -> str:
        """Generate a villain name."""
        style = random.choice(["prefix_title", "title_noun", "the_noun", "simple"])
        
        if style == "prefix_title":
            return f"{random.choice(self.PREFIXES)} {random.choice(self.TITLES)}"
        elif style == "title_noun":
            return f"{random.choice(self.TITLES)} of {random.choice(self.NOUNS)}"
        elif style == "the_noun":
            return f"The {random.choice(self.NOUNS)}"
        else:
            return f"{random.choice(self.NOUNS)} {random.choice(self.TITLES)}"
    
    def _describe_from_traits(self, traits: Dict[str, float]) -> str:
        """Generate description from traits."""
        descriptions = []
        
        if traits["aggression"] > 0.7:
            descriptions.append("fiercely aggressive")
        elif traits["aggression"] < 0.3:
            descriptions.append("remarkably passive")
        
        if traits["patience"] > 0.7:
            descriptions.append("extremely patient")
        elif traits["patience"] < 0.3:
            descriptions.append("impulsive and quick-tempered")
        
        if traits["chaos"] > 0.7:
            descriptions.append("chaotically unpredictable")
        elif traits["chaos"] < 0.3:
            descriptions.append("methodically consistent")
        
        if traits["adaptability"] > 0.7:
            descriptions.append("highly adaptable")
        
        if traits["caution"] > 0.7:
            descriptions.append("extremely cautious")
        elif traits["caution"] < 0.3:
            descriptions.append("recklessly daring")
        
        if not descriptions:
            return "A balanced opponent with varied tactical approaches."
        
        return f"A {' who '.join(descriptions)} villain."
    
    def list_archetypes(self) -> list:
        """List available archetypes."""
        return list(self.ARCHETYPES.keys())
