import pytest
from unittest.mock import patch
from src.backend_codebase.ai_integration import generate_content

@patch('src.backend_codebase.ai_integration.openai.Completion.create')
def test_generate_content(mock_create):
    mock_create.return_value = {'choices': [{'text': 'Generated content'}]}
    prompt = "Test prompt"
    result = generate_content(prompt)
    assert result == 'Generated content'
    mock_create.assert_called_once_with(
        prompt=prompt,
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
