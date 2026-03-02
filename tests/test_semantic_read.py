import pytest
from agent.tools.semantic_read import read_code_element

def test_read_code_element():
    """Test reading a code element."""
    # Arrange
    test_input = "example_code_element"
    expected_output = "parsed_element"
    
    # Act
    result = read_code_element(test_input)
    
    # Assert
    assert result == expected_output