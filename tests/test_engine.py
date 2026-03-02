import pytest
from src.server.engine import run_agent_sync

def test_run_agent_sync():
    """Test run_agent_sync function."""
    result = run_agent_sync()
    assert result is not None
