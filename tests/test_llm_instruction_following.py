import pytest

def test_create_improved_instruction():
    """Test instruction improvement logic."""
    # Arrange
    original_instruction = "Write a summary"
    expected_improved = "Write a concise 3-sentence summary"
    
    # Act
    result = create_improved_instruction(original_instruction)
    
    # Assert
    assert result == expected_improved
