import pytest

from agent.test_surface_mapper import map_pr_to_test_surface

def test_map_pr_to_test_surface():
    """Test mapping PR to test surface."""
    # Arrange
    pr_data = {"changes": ["file1.py", "file2.py"]}
    expected_surface = ["test_file1.py", "test_file2.py"]
    
    # Act
    result = map_pr_to_test_surface(pr_data)
    
    # Assert
    assert result == expected_surface
