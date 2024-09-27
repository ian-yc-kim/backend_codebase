import pytest
from unittest.mock import patch
from src.backend_codebase.ai_integration import generate_content

@patch('src.backend_codebase.ai_integration.openai.Completion.create')
def test_generate_content(mock_create):
    mock_create.return_value.choices = [type('', (object,), {'text': 'Generated content'})()]
    prompt = "Test prompt"
    result = generate_content(prompt)
    assert result == 'Generated content'
    mock_create.assert_called_once_with(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )
