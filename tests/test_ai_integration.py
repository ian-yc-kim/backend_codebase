import pytest
from src.backend_codebase.ai_integration import AIIntegration

@pytest.fixture
def ai_integration():
    return AIIntegration()


def test_update_state(ai_integration):
    ai_integration.update_state("New state")
    assert ai_integration.current_state == "New state"


def test_update_feedback(ai_integration):
    ai_integration.update_feedback("New feedback")
    assert ai_integration.user_feedback == "New feedback"


def test_generate_new_content(mocker, ai_integration):
    mocker.patch('src.backend_codebase.ai_integration.generate_content', return_value="Generated content")
    ai_integration.update_state("State")
    ai_integration.update_feedback("Feedback")
    new_content = ai_integration.generate_new_content()
    assert new_content == "Generated content"
