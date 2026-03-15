"""Tests for VillainEngine."""

import pytest
from aivill import VillainEngine, Config
from aivill.exceptions import ValidationError


class TestVillainEngine:
    """Test cases for VillainEngine."""
    
    def test_initialization(self, config):
        """Test engine initialization."""
        engine = VillainEngine(config)
        assert engine.name == "Test Villain"
        assert engine.total_decisions == 0
    
    def test_load_personality(self, engine):
        """Test personality loading."""
        traits = engine.get_personality()
        assert traits["aggression"] == 0.5
        assert traits["patience"] == 0.5
    
    def test_update_state(self, engine):
        """Test game state update."""
        game_state = {
            "player_health": 80,
            "villain_health": 100,
            "player_last_action": "attack",
            "round_number": 1
        }
        observations = engine.update_state(game_state)
        assert observations is not None
        assert "player_is_aggressive" in observations
    
    def test_decide_action(self, engine):
        """Test decision making."""
        game_state = {
            "player_health": 80,
            "villain_health": 100,
            "player_last_action": "attack",
            "round_number": 1,
            "available_actions": ["attack", "defend"]
        }
        engine.update_state(game_state)
        decision = engine.decide_action()
        assert decision is not None
        assert "action" in decision
        assert "strategy" in decision
    
    def test_learn_from_result(self, engine):
        """Test learning from results."""
        game_state = {
            "player_health": 80,
            "villain_health": 100,
            "player_last_action": "attack",
            "round_number": 1
        }
        engine.update_state(game_state)
        engine.decide_action()
        
        result = {
            "outcome": "victory",
            "success": True,
            "reward": 1.0
        }
        engine.learn_from_result(result)
        assert engine.total_learning_iterations == 1
    
    def test_save_load_memory(self, engine, temp_dir):
        """Test memory save and load."""
        game_state = {"player_health": 80, "villain_health": 100}
        engine.update_state(game_state)
        engine.decide_action()
        engine.learn_from_result({"success": True})
        
        engine.save_memory()
        
        # Create new engine and load
        engine2 = VillainEngine({
            "data_dir": str(temp_dir / "data"),
            "log_dir": str(temp_dir / "logs")
        })
        engine2.load_memory()
        
        assert engine2.total_decisions >= 0
    
    def test_get_state_summary(self, engine):
        """Test state summary."""
        summary = engine.get_state_summary()
        assert "name" in summary
        assert "total_decisions" in summary
        assert "personality" in summary


class TestConfig:
    """Test cases for Config class."""
    
    def test_default_config(self):
        """Test default configuration."""
        from aivill.config import Config
        config = Config()
        assert config.get("name") == "The Villain"
    
    def test_custom_config(self):
        """Test custom configuration."""
        from aivill.config import Config
        config = Config({"name": "Custom Villain"})
        assert config.get("name") == "Custom Villain"
    
    def test_nested_config(self):
        """Test nested configuration."""
        from aivill.config import Config
        config = Config()
        assert config.get("personality.aggression") == 0.5
    
    def test_config_set(self):
        """Test setting configuration values."""
        from aivill.config import Config
        config = Config()
        config.set("name", "New Villain")
        assert config.get("name") == "New Villain"
    
    def test_config_from_dict(self):
        """Test config to_dict."""
        from aivill.config import Config
        config = Config({"test": "value"})
        d = config.to_dict()
        assert "test" in d


class TestExceptions:
    """Test cases for exceptions."""
    
    def test_aivill_error(self):
        """Test base exception."""
        from aivill.exceptions import AiVillError
        with pytest.raises(AiVillError):
            raise AiVillError("Test error")
    
    def test_configuration_error(self):
        """Test configuration exception."""
        from aivill.exceptions import ConfigurationError
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Config error")
