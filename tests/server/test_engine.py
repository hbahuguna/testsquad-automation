import pytest
from src.server.engine import SquadEngine


def def test_run_agent_sync_returns_string_response():
    """Tests that the run_agent_sync method returns a non-empty string response."""
    # Arrange
    engine = SquadEngine()
    test_task = "What is the capital of Spain?"

    # Act
    # Assuming run_agent_sync is a sync method on SquadEngine that takes a task string.
    response = engine.run_agent_sync(task=test_task)

    # Assert
    assert isinstance(response, str)
    assert response
