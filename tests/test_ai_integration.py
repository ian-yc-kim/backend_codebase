from unittest.mock import patch
from src.backend_codebase.ai_integration import generate_content

@patch('src.backend_codebase.ai_integration.openai_client.chat_completions_create')
def test_generate_content(mock_chat_completions_create):
    mock_response = 'Mocked response content'
    mock_chat_completions_create.return_value = mock_response
    prompt = 'Test prompt'
    content = generate_content(prompt)
    assert content == mock_response
