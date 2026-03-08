import pytest
from src.agent.context_pruner import ContextPruner


def test_build_dependency_context_string_with_dependencies():
    """
    Tests that the dependency context string is built correctly for a non-empty dictionary.
    """
    # Arrange
    dependencies = {
        "src/main.py": "import utils\n\nprint(utils.add(1, 2))",
        "src/utils.py": "def add(a, b):\n    return a + b"
    }
    # Assuming order is preserved (Python 3.7+ dicts)
    expected_string = (
        "File: src/main.py\n---\nimport utils\n\nprint(utils.add(1, 2))\n---\n"
        "File: src/utils.py\n---\ndef add(a, b):\n    return a + b\n---"
    )

    # Act
    # Assuming build_dependency_context_string is a static method as it's a utility function.
    result_string = ContextPruner.build_dependency_context_string(dependencies)

    # Assert
    assert result_string == expected_string


def test_build_dependency_context_string_empty_dict():
    """
    Tests that an empty string is returned when the dependency dictionary is empty.
    """
    # Arrange
    dependencies = {}

    # Act
    result_string = ContextPruner.build_dependency_context_string(dependencies)

    # Assert
    assert result_string == ""


def test_build_dependency_context_string_with_empty_content():
    """
    Tests that files with empty content are handled correctly in the context string.
    """
    # Arrange
    dependencies = {
        "src/main.py": "import utils",
        "src/empty.py": ""
    }
    expected_string = (
        "File: src/main.py\n---\nimport utils\n---\n"
        "File: src/empty.py\n---\n\n---"
    )

    # Act
    result_string = ContextPruner.build_dependency_context_string(dependencies)

    # Assert
    assert result_string == expected_string


def test_build_dependency_context_string_with_none_input():
    """
    Tests that a TypeError is raised when the input is None, which is invalid.
    """
    # Arrange
    # No arrangement needed for this test case.

    # Act & Assert
    with pytest.raises(TypeError):
        ContextPruner.build_dependency_context_string(None)
