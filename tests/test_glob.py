import pytest
from src.agent.tools.glob import glob

def test_glob():
    """Test glob functionality."""
    result = glob('*.py')
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)