import pytest
from src.server.engine import SquadEngine


@pytest.mark.asyncio
async def test_a_chat_returns_string_response():
    """Tests that the a_chat method returns a non-empty string response."""
    # Arrange
    engine = SquadEngine()
    test_messages = [{"role": "user", "content": "What is the capital of France?"}]

    # Act
    # Assuming a_chat is an async method on SquadEngine that takes a list of messages.
    response = await engine.a_chat(messages=test_messages)

    # Assert
    assert isinstance(response, str)
    assert response
