import pytest
from src.backend_codebase.services import generate_character_profile
from unittest.mock import patch


def test_generate_character_profile():
    character_name = 'John Doe'
    traits = 'Brave, Smart'
    backstory = 'A hero from a small village'
    with patch('openai.Completion.create') as mock_openai:
        mock_openai.return_value = type('obj', (object,), {
            'choices': [type('obj', (object,), {'text': 'Mocked profile for John Doe'})]
        })
        profile = generate_character_profile(character_name, traits, backstory)
        assert isinstance(profile, str)
        assert profile == 'Mocked profile for John Doe'


def test_generate_character_profile_missing_fields():
    with pytest.raises(ValueError):
        generate_character_profile('', 'Brave, Smart', 'A hero from a small village')
    with pytest.raises(ValueError):
        generate_character_profile('John Doe', '', 'A hero from a small village')
    with pytest.raises(ValueError):
        generate_character_profile('John Doe', 'Brave, Smart', '')
