import pytest
from src.server.prompt_manager import wait_for_answer

class TestPromptManager:
    def test_wait_for_answer(self):
        """Test waiting for an answer functionality."""
        # Assuming wait_for_answer takes a prompt and returns a response
        prompt = 'example_prompt'
        expected_response = 'Expected response'
        assert wait_for_answer(prompt) == expected_response
