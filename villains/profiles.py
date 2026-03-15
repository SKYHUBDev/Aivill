"""
Pre-made villain profiles for quick use.
"""

VILLAIN_PROFILES = {
    "trap_master": {
        "name": "The Trap Master",
        "aggression": 0.3,
        "patience": 0.9,
        "ego": 0.5,
        "chaos": 0.2,
        "adaptability": 0.8,
        "caution": 0.7,
        "description": "Patient and cunning, this villain sets elaborate traps based on observed patterns."
    },
    "chaos_overlord": {
        "name": "Chaos Overlord",
        "aggression": 0.9,
        "patience": 0.2,
        "ego": 0.9,
        "chaos": 0.95,
        "adaptability": 0.4,
        "caution": 0.1,
        "description": "An unpredictable force of destruction who thrives on chaos and confusion."
    },
    "mind_reader": {
        "name": "The Mind Reader",
        "aggression": 0.4,
        "patience": 0.9,
        "ego": 0.5,
        "chaos": 0.05,
        "adaptability": 0.95,
        "caution": 0.5,
        "description": "A master psychologist who predicts and counters every player move."
    },
    "berserker": {
        "name": "The Berserker",
        "aggression": 0.95,
        "patience": 0.1,
        "ego": 0.85,
        "chaos": 0.5,
        "adaptability": 0.3,
        "caution": 0.05,
        "description": "A relentless warrior who knows only forward, never back."
    },
    "turtle": {
        "name": "The Iron Turtle",
        "aggression": 0.15,
        "patience": 0.95,
        "ego": 0.3,
        "chaos": 0.05,
        "adaptability": 0.4,
        "caution": 0.98,
        "description": "An almost impenetrable defense that waits for mistakes."
    },
    "trickster": {
        "name": "The Trickster",
        "aggression": 0.4,
        "patience": 0.6,
        "ego": 0.7,
        "chaos": 0.75,
        "adaptability": 0.85,
        "caution": 0.25,
        "description": "A deceptive mastermind who misleads and confuses opponents."
    },
    "sadist": {
        "name": "The Sadist",
        "aggression": 0.7,
        "patience": 0.7,
        "ego": 0.8,
        "chaos": 0.5,
        "adaptability": 0.6,
        "caution": 0.3,
        "description": "A cruel villain who enjoys toying with victims before finishing them."
    },
    "mercenary": {
        "name": "The Mercenary",
        "aggression": 0.5,
        "patience": 0.5,
        "ego": 0.4,
        "chaos": 0.3,
        "adaptability": 0.92,
        "caution": 0.6,
        "description": "A practical fighter who quickly adapts tactics to counter opponents."
    },
    "egomaniac": {
        "name": "The Egomaniac",
        "aggression": 0.6,
        "patience": 0.25,
        "ego": 0.99,
        "chaos": 0.15,
        "adaptability": 0.35,
        "caution": 0.35,
        "description": "An arrogant villain who underestimates opponents due to supreme confidence."
    },
    "shadow": {
        "name": "The Shadow",
        "aggression": 0.3,
        "patience": 0.85,
        "ego": 0.5,
        "chaos": 0.15,
        "adaptability": 0.9,
        "caution": 0.85,
        "description": "A stealthy hunter who observes, learns, and strikes without warning."
    }
}


def load_villain(name: str) -> dict:
    """Load a pre-made villain profile."""
    return VILLAIN_PROFILES.get(name.lower())


def list_villains() -> list:
    """List all available villain profiles."""
    return list(VILLAIN_PROFILES.keys())
