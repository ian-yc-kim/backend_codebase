import pytest
from unittest.mock import patch
from backend_codebase.ai_integration import generate_content


def test_generate_content():
    prompt = 'Once upon a time'

    # Patch the openai.ChatCompletion.create method
    with patch('backend_codebase.ai_integration.openai.ChatCompletion.create') as mock_create:
        # Set up the mock to return a specific value
        mock_create.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Generated content based on the prompt.'
                    }
                }
            ]
        }

        content = generate_content(prompt)
        assert content == 'Generated content based on the prompt.'
