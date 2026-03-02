import pytest
from src.agent.test_generator import generate_tests_with_reasoning

def test_generate_tests_with_reasoning():
    """Test the generate_tests_with_reasoning function."""
    result = generate_tests_with_reasoning()
    assert result is not None
