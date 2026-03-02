import pytest
from src.ci.pr_runner import run_agent_on_pr

@pytest.fixture
def mock_pr_data():
    return {
        "number": 49,
        "title": "Test PR",
        "body": "Test PR description",
        "state": "open",
        "head": {
            "ref": "test-branch",
            "sha": "abc123"
        },
        "base": {
            "ref": "main",
            "sha": "def456"
        }
    }

def test_run_agent_on_pr(mock_pr_data):
    """Test running agent on PR data."""
    result = run_agent_on_pr(mock_pr_data)
    assert result is not None
    assert isinstance(result, dict)
    assert "status" in result
    assert "details" in result
