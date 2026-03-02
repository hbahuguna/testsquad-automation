import pytest
from src.agent.core import run_with_tools

def test_run_with_tools():
    """Test running the agent with tools."""
    with pytest.raises(FileNotFoundError):
        run_with_tools('non_existent_file.txt')
