import pytest
from pathlib import Path
from unittest.mock import patch

# Assuming the source file is located at 'src/config.py'
from src.config import AgentConfig, HAS_YAML


def test_load_from_file_not_found():
    """
    Test that load_from_file raises FileNotFoundError for a non-existent file.
    """
    # Arrange
    non_existent_path = Path("this/path/does/not/exist.yaml")

    # Act & Assert
    with pytest.raises(FileNotFoundError, match="Config file not found"):
        AgentConfig.load_from_file(non_existent_path)


def test_load_from_file_empty_file(tmp_path: Path):
    """
    Test that loading an empty config file results in a default AgentConfig.
    """
    # Arrange
    config_file = tmp_path / "config.yaml"
    config_file.write_text("")
    expected_config = AgentConfig.default()

    # Act
    loaded_config = AgentConfig.load_from_file(config_file)

    # Assert
    assert loaded_config == expected_config


@pytest.mark.skipif(not HAS_YAML, reason="pyyaml is not installed, cannot test YAMLError")
def test_load_from_file_invalid_yaml_with_pyyaml(tmp_path: Path):
    """
    Test that a ValueError is raised for malformed YAML when pyyaml is installed.
    """
    # Arrange
    config_file = tmp_path / "config.yaml"
    # This is invalid YAML because of the unindented list item
    config_file.write_text("model: gpt-4\n tools: \n- tool1\n-tool2")

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid YAML"):
        AgentConfig.load_from_file(config_file)


def test_load_from_file_tools_not_a_list(tmp_path: Path):
    """
    Test that a ValueError is raised if the 'tools' key is not a list.
    """
    # Arrange
    config_file = tmp_path / "config.yaml"
    config_file.write_text("tools: not-a-list")

    # Act & Assert
    with pytest.raises(ValueError, match="'tools' must be a list, got <class 'str'>"):
        AgentConfig.load_from_file(config_file)


def test_load_from_file_with_unknown_keys(tmp_path: Path):
    """
    Test that unknown keys in the config file are ignored.
    """
    # Arrange
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
        model: gpt-4-turbo
        unknown_key: some_value
        another_key: 123
        """
    )
    expected_config = AgentConfig(model="gpt-4-turbo")

    # Act
    loaded_config = AgentConfig.load_from_file(config_file)

    # Assert
    assert loaded_config.model == expected_config.model
    assert loaded_config.temperature == AgentConfig.default().temperature
    assert loaded_config.tools == AgentConfig.default().tools


def test_load_from_file_type_coercion_error(tmp_path: Path):
    """
    Test that a ValueError is raised if a value cannot be coerced to the correct type.
    """
    # Arrange
    config_file = tmp_path / "config.yaml"
    config_file.write_text("max_tokens: not-an-int")

    # Act & Assert
    with pytest.raises(ValueError, match="invalid literal for int()"):
        AgentConfig.load_from_file(config_file)


def test_load_from_file_invalid_timeout_value(tmp_path: Path):
    """
    Test that a ValueError is raised if timeout_seconds is not a valid float.
    """
    # Arrange
    config_file = tmp_path / "config.yaml"
    config_file.write_text("timeout_seconds: not-a-float")

    # Act & Assert
    with pytest.raises(ValueError, match="could not convert string to float"):
        AgentConfig.load_from_file(config_file)


@patch("src.config.HAS_YAML", False)
@patch("src.config.yaml", None)
def test_load_from_file_no_pyyaml_fallback_parser(tmp_path: Path):
    """
    Test the fallback parser when pyyaml is not installed.
    """
    # Arrange
    config_file = tmp_path / "config.yaml"
    # The fallback parser is more strict about formatting, requiring JSON-like values.
    config_content = '''
tools: ["tool1", "tool2"]
temperature: 0.7
model: "custom-model"
max_tokens: 1024
seed: 42
timeout_seconds: 60.5
provider: "openai"
base_url: "https://api.example.com"
'''
    config_file.write_text(config_content)
    expected_config = AgentConfig(
        tools=["tool1", "tool2"],
        temperature=0.7,
        model="custom-model",
        max_tokens=1024,
        seed=42,
        timeout_seconds=60.5,
        provider="openai",
        base_url="https://api.example.com",
    )

    # Act
    loaded_config = AgentConfig.load_from_file(config_file)

    # Assert
    assert loaded_config == expected_config
