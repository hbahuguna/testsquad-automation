import pytest
from src.agent.context_pruner import ContextPruner

def test_context_pruner_init():
    """
    Tests that the ContextPruner class can be initialized successfully.

    This test assumes a default constructor with no required arguments. If the
    __init__ method requires parameters, this test will fail and should be
    updated to reflect the new signature.
    """
    # Arrange
    # No specific arrangement is needed for default initialization.

    # Act
    instance = ContextPruner()

    # Assert
    assert isinstance(instance, ContextPruner), "Object should be an instance of ContextPruner"
