import pytest
from unittest.mock import patch
from src.backend_codebase.services import generate_chapter_content

@patch('src.backend_codebase.services.openai.Completion.create')
def test_generate_chapter_content(mock_openai_create):
    mock_openai_create.return_value.choices = [type('', (object,), {'text': 'Generated content'})()]

    title = 'Test Title'
    previous_content = 'Previous content'
    user_prompts = 'User prompts'

    content = generate_chapter_content(title, previous_content, user_prompts)

    assert content == 'Generated content'

@patch('src.backend_codebase.services.openai.Completion.create')
def test_generate_chapter_content_missing_params(mock_openai_create):
    with pytest.raises(ValueError):
        generate_chapter_content('', 'Previous content', 'User prompts')
    with pytest.raises(ValueError):
        generate_chapter_content('Test Title', '', 'User prompts')
    with pytest.raises(ValueError):
        generate_chapter_content('Test Title', 'Previous content', '')

@patch('src.backend_codebase.services.openai.Completion.create')
def test_generate_chapter_content_api_error(mock_openai_create):
    mock_openai_create.side_effect = Exception('API error')

    with pytest.raises(RuntimeError) as excinfo:
        generate_chapter_content('Test Title', 'Previous content', 'User prompts')

    assert 'Failed to generate content: API error' in str(excinfo.value)
