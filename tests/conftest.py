"""Pytest configuration and fixtures."""

import pytest
import tempfile
import shutil
from pathlib import Path

from aivill import VillainEngine


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp = tempfile.mkdtemp()
    yield Path(temp)
    shutil.rmtree(temp)


@pytest.fixture
def config(temp_dir):
    """Create test configuration."""
    return {
        "name": "Test Villain",
        "data_dir": str(temp_dir / "data"),
        "log_dir": str(temp_dir / "logs"),
        "llm_model": "phi3.5",
        "personality": {
            "aggression": 0.5,
            "patience": 0.5,
            "ego": 0.5,
            "chaos": 0.5,
            "adaptability": 0.5,
            "caution": 0.5,
        }
    }


@pytest.fixture
def engine(config):
    """Create a VillainEngine instance."""
    eng = VillainEngine(config)
    eng.load_personality({"traits": config["personality"]})
    return eng
