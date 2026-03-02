import pytest
from src.agent.tools.grep import grep

def test_grep():
    """Test grep functionality."""
    lines = ['apple', 'banana', 'cherry']
    pattern = 'banana'
    result = grep(pattern, lines)
    assert result == ['banana']
