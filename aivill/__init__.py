"""
AiVill - A modular self-learning villain AI engine.

AiVill provides adaptive, self-learning villain AI that can be integrated
into any game with minimal effort.

Example:
    >>> from aivill import VillainEngine
    >>> 
    >>> engine = VillainEngine()
    >>> engine.initialize({"data_dir": "data"})
    >>> engine.update_state({"player_health": 80, "villain_health": 100})
    >>> decision = engine.decide_action()
    >>> engine.learn_from_result({"outcome": "victory", "success": True})

For more information, see: https://github.com/aivill/aivill
"""

__version__ = "0.1.0"
__author__ = "AiVill Team"
__license__ = "MIT"

# Public API exports
from aivill.core.engine import VillainEngine
from aivill.config import Config, default_config
from aivill.exceptions import (
    AiVillError,
    ConfigurationError,
    MemoryError,
    PersonalityError,
    StrategyError,
    LearningError,
    LLMError,
    OllamaNotAvailableError,
    DecisionError,
    PerceptionError,
    ValidationError,
)

__all__ = [
    # Core
    "VillainEngine",
    "Config",
    "default_config",
    # Exceptions
    "AiVillError",
    "ConfigurationError",
    "MemoryError",
    "PersonalityError",
    "StrategyError",
    "LearningError",
    "LLMError",
    "OllamaNotAvailableError",
    "DecisionError",
    "PerceptionError",
    "ValidationError",
    # Version
    "__version__",
]
