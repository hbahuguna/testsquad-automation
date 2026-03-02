import pytest
from src.agent.tools.ask_human import ask_human

def test_ask_human():
    """Test ask_human function."""
    result = ask_human("What is your name?")
    assert result is not None
