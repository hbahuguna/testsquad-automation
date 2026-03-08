import pytest
from unittest.mock import patch

# Assume src.llm.client exists and has a class LLMClient with a from_environment method
# This test file is written against the presumed behavior of such a method.
from src.llm.client import LLMClient


class TestFromEnvironment:
    """Tests for the LLMClient.from_environment class method."""

    def test_from_environment_success_with_all_vars(self, monkeypatch):
        """Test successful client creation when all environment variables are set."""
        # Arrange
        monkeypatch.setenv("LLM_API_KEY", "test_api_key_123")
        monkeypatch.setenv("LLM_BASE_URL", "https://api.test.com")
        monkeypatch.setenv("LLM_TIMEOUT", "60")

        # Act
        client = LLMClient.from_environment()

        # Assert
        assert isinstance(client, LLMClient)
        assert client.api_key == "test_api_key_123"
        assert client.base_url == "https://api.test.com"
        assert client.timeout == 60

    def test_from_environment_missing_required_variable_raises_error(self, monkeypatch):
        """Test that a ValueError is raised if a required environment variable is missing."""
        # Arrange
        # Ensure the required key is not in the environment
        monkeypatch.delenv("LLM_API_KEY", raising=False)
        monkeypatch.setenv("LLM_BASE_URL", "https://api.test.com")

        # Act & Assert
        with pytest.raises(ValueError, match="LLM_API_KEY environment variable not set"):
            LLMClient.from_environment()

    def test_from_environment_uses_default_values(self, monkeypatch):
        """Test that default values are used for optional environment variables when they are not set."""
        # Arrange
        monkeypatch.setenv("LLM_API_KEY", "test_api_key_456")
        # Unset optional variables to ensure defaults are used
        monkeypatch.delenv("LLM_BASE_URL", raising=False)
        monkeypatch.delenv("LLM_TIMEOUT", raising=False)

        # Act
        client = LLMClient.from_environment()

        # Assert
        assert client.api_key == "test_api_key_456"
        # Assuming default values for base_url and timeout
        assert client.base_url == "https://api.example.com"
        assert client.timeout == 30

    def test_from_environment_invalid_timeout_value_raises_error(self, monkeypatch):
        """Test that a ValueError is raised for a non-integer timeout value."""
        # Arrange
        monkeypatch.setenv("LLM_API_KEY", "test_api_key_789")
        monkeypatch.setenv("LLM_TIMEOUT", "not-an-integer")

        # Act & Assert
        with pytest.raises(ValueError, match="LLM_TIMEOUT must be an integer"):
            LLMClient.from_environment()

    def test_from_environment_empty_api_key_raises_error(self, monkeypatch):
        """Test that an empty string for a required variable is treated as missing and raises an error."""
        # Arrange
        monkeypatch.setenv("LLM_API_KEY", "")

        # Act & Assert
        with pytest.raises(ValueError, match="LLM_API_KEY environment variable not set"):
            LLMClient.from_environment()
