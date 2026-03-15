"""
Custom exceptions for AiVill.
"""


class AiVillError(Exception):
    """Base exception for all AiVill errors."""
    pass


class ConfigurationError(AiVillError):
    """Raised when there's an issue with configuration."""
    pass


class MemoryError(AiVillError):
    """Raised when there's an issue with memory operations."""
    pass


class PersonalityError(AiVillError):
    """Raised when there's an issue with personality operations."""
    pass


class StrategyError(AiVillError):
    """Raised when there's an issue with strategy operations."""
    pass


class LearningError(AiVillError):
    """Raised when there's an issue with learning operations."""
    pass


class LLMError(AiVillError):
    """Raised when there's an issue with LLM operations."""
    pass


class OllamaNotAvailableError(LLMError):
    """Raised when Ollama is not available."""
    pass


class DecisionError(AiVillError):
    """Raised when there's an issue with decision making."""
    pass


class PerceptionError(AiVillError):
    """Raised when there's an issue with perception."""
    pass


class ValidationError(AiVillError):
    """Raised when input validation fails."""
    pass
