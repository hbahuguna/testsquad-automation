import pytest
from ui.src.hooks.useChat import useChat

def test_useChat_returns_valid_structure():
    """Test that useChat hook returns an object with expected structure."""
    result = useChat()
    assert isinstance(result, dict), "Result should be a dictionary"
    assert 'messages' in result, "Result should contain 'messages' key"
    assert isinstance(result['messages'], list), "'messages' should be a list"
    assert 'sendMessage' in result, "Result should contain 'sendMessage' key"
    assert callable(result['sendMessage']), "'sendMessage' should be callable"
