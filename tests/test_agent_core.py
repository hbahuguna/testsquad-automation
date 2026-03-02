import pytest
from src.agent.core import AgentCore

@pytest.fixture
def agent_core_instance():
    return AgentCore()

def test_agent_core_initialization(agent_core_instance):
    assert agent_core_instance is not None
