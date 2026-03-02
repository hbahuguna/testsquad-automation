import pytest
from ui.src.components.ChatConsole import ChatConsole

def test_chat_console_renders():
    """Test that ChatConsole component renders correctly."""
    console = ChatConsole()
    assert console is not None
    # Add more assertions based on component behavior
