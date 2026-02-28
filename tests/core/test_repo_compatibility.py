import pytest
import shutil
import tempfile
import yaml
from pathlib import Path
from unittest.mock import patch, Mock
from src.ci.pr_runner import run_agent_on_pr
from mcp.automation_repo import AutomationRepoMCP

@pytest.fixture
def mock_workspaces():
    """Creates a temporary product and automation repository structure for testing."""
    with tempfile.TemporaryDirectory() as prod_dir, tempfile.TemporaryDirectory() as auto_dir:
        prod_path = Path(prod_dir)
        auto_path = Path(auto_dir)
        
        # Init product logic
        (prod_path / "src").mkdir()
        (prod_path / "src" / "core.py").write_text("def logic(): pass")
        
        # Init auto logic
        auto_testsquad = auto_path / ".testsquad"
        auto_testsquad.mkdir()
        
        (auto_path / "tests").mkdir()
        
        yield prod_path, auto_path

@patch("subprocess.run")
@patch("src.ci.pr_runner.map_pr_to_test_surface")
def test_repo_compatibility_matching_repos(mock_map, mock_run, mock_workspaces):
    """
    Scenario: Product repo matches defined target repository in automation configuration
    """
    prod_path, auto_path = mock_workspaces
    
    # Mock git origin to return a specific repository string
    mock_run.return_value = Mock(stdout="hbahuguna/testsquad\n")
    mock_map.return_value = {"covered_behaviors": [], "uncovered_behaviors": []}
    
    # Create the config.yaml that matches
    config_file = auto_path / ".testsquad" / "config.yaml"
    config_file.write_text(yaml.dump({"target_repo": "hbahuguna/testsquad"}))
    
    result = run_agent_on_pr("1", prod_path, auto_path, use_real_git=False, use_real_fs=False)
    assert result["status"] == "pass"

@patch("subprocess.run")
def test_repo_compatibility_mismatched_repos(mock_run, mock_workspaces):
    """
    Scenario: Product repo mismatches the defined target repository
    """
    prod_path, auto_path = mock_workspaces
    
    # Mock git origin to return a completely different repository string
    mock_run.return_value = Mock(stdout="hbahuguna/legacy-app\n")
    
    # Create the config.yaml that points to testsquad
    config_file = auto_path / ".testsquad" / "config.yaml"
    config_file.write_text(yaml.dump({"target_repo": "hbahuguna/testsquad"}))
    
    result = run_agent_on_pr("1", prod_path, auto_path, use_real_git=False, use_real_fs=False)
    
    assert result["status"] == "fail"
    assert "Configuration Mismatch" in result["error"]
    assert result["state"] == "FAILED"

def test_test_discovery_tags_correctly(mock_workspaces):
    """
    Scenario: Test Discovery correctly tags Unit vs E2E tests
    """
    _, auto_path = mock_workspaces
    
    # Must be placed in a directory search_tests_real looks into
    tests_dir = auto_path / "tests"
    
    api_test = tests_dir / "test_api.py"
    api_test.write_text("import pytest\ndef test_backend(): pass")
    
    ui_test = tests_dir / "test_ui_flow.spec.ts"
    ui_test.write_text("import { test } from '@playwright/test';\ntest('login', async ({ page }) => {});")
    
    mcp = AutomationRepoMCP(str(auto_path), use_real_fs=True)
    tests = mcp.search_tests({})  # triggers search_tests_real
    
    # Find the tagged tests
    types_found = {Path(t["file"]).name: t.get("type") for t in tests}
    
    assert "test_ui_flow.spec.ts" in types_found
    assert "test_api.py" in types_found
    assert types_found["test_ui_flow.spec.ts"] == "e2e"
    assert types_found["test_api.py"] == "unit"
