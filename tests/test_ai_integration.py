import pytest
from backend_codebase.ai_integration import generate_content, OpenAIError


def test_generate_content_success(mocker):
    mocker.patch('backend_codebase.ai_integration.openai.ChatCompletion.create', return_value=mocker.Mock(choices=[mocker.Mock(message={'content': 'Generated content'})]))
    result = generate_content('Test prompt')
    assert result == 'Generated content'


def test_generate_content_failure(mocker):
    mocker.patch('backend_codebase.ai_integration.openai.ChatCompletion.create', side_effect=OpenAIError('An error occurred'))
    with pytest.raises(OpenAIError):
        generate_content('Test prompt')
