from src.agent.test_surface_mapper import map_pr_to_test_surface


class MockPullRequest:
    """A mock object to simulate a Pull Request object."""

    def __init__(self, changed_files):
        self.changed_files = changed_files


def test_map_pr_to_test_surface_identifies_source_files():
    """
    Tests that map_pr_to_test_surface correctly identifies Python source files
    from a list of mixed file types in a PR, excluding test files and non-Python files.
    """
    # Arrange: Create a mock PR with a variety of changed file paths
    mock_pr = MockPullRequest(changed_files=[
        "src/agent/main.py",
        "src/utils/helpers.py",
        "tests/agent/test_main.py",
        "README.md",
        ".github/workflows/ci.yml"
    ])

    expected_test_surface = [
        "src/agent/main.py",
        "src/utils/helpers.py"
    ]

    # Act: Call the target function
    actual_test_surface = map_pr_to_test_surface(mock_pr)

    # Assert: Verify the output contains only the source files
    # Use set comparison for order-insensitivity
    assert set(actual_test_surface) == set(expected_test_surface)
