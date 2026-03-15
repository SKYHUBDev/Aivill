"""
Configuration system for AiVill.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from aivill.exceptions import ConfigurationError


class Config:
    """
    Configuration manager for AiVill.
    
    Handles loading and validation of configuration from various sources.
    """
    
    DEFAULT_CONFIG = {
        "name": "The Villain",
        "data_dir": "data",
        "log_dir": "logs",
        "llm_model": "phi3.5",
        "llm_enabled": True,
        "llm_temperature": 0.7,
        "llm_max_tokens": 200,
        "personality": {
            "aggression": 0.5,
            "patience": 0.5,
            "ego": 0.5,
            "chaos": 0.5,
            "adaptability": 0.5,
            "caution": 0.5,
        },
        "learning": {
            "learning_rate": 0.1,
            "discount_factor": 0.9,
            "exploration_rate": 0.1,
        },
        "memory": {
            "max_short_term_items": 100,
            "save_interval": 10,
        },
        "strategy": {
            "mutation_rate": 0.1,
            "min_effectiveness": 0.3,
        },
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize configuration.
        
        Args:
            config: Optional configuration dictionary to merge with defaults
        """
        self._config = self.DEFAULT_CONFIG.copy()
        
        if config:
            self.update(config)
    
    def update(self, config: Dict[str, Any]) -> None:
        """
        Update configuration with new values.
        
        Args:
            config: Configuration dictionary to merge
        """
        self._deep_update(self._config, config)
    
    def _deep_update(self, base: Dict, update: Dict) -> None:
        """Recursively update nested dictionaries."""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., "personality.aggression")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., "personality.aggression")
            value: Value to set
        """
        keys = key.split(".")
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self._config.copy()
    
    @classmethod
    def from_file(cls, path: str) -> "Config":
        """
        Load configuration from JSON file.
        
        Args:
            path: Path to configuration file
            
        Returns:
            Config instance
            
        Raises:
            ConfigurationError: If file cannot be loaded
        """
        try:
            with open(path, "r") as f:
                config = json.load(f)
            return cls(config)
        except FileNotFoundError:
            raise ConfigurationError(f"Configuration file not found: {path}")
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration file: {e}")
    
    @classmethod
    def from_env(cls, prefix: str = "AIVILL_") -> "Config":
        """
        Load configuration from environment variables.
        
        Args:
            prefix: Environment variable prefix
            
        Returns:
            Config instance
        """
        import os
        
        config = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                
                # Handle nested keys
                parts = config_key.split("_")
                if len(parts) > 1:
                    current = config
                    for part in parts[:-1]:
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                    current[parts[-1]] = value
                else:
                    config[config_key] = value
        
        return cls(config)


# Global default configuration
default_config = Config()
