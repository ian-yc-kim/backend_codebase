import pytest
from src.backend_codebase.services import generate_plot_twist


def test_generate_plot_twist_success(mocker):
    mock_openai = mocker.patch('src.backend_codebase.services.openai.Completion.create')
    mock_openai.return_value.choices = [mocker.Mock(text='A surprising plot twist!')]

    current_plot = 'The hero is on a quest.'
    user_suggestions = 'Introduce a new villain.'
    result = generate_plot_twist(current_plot, user_suggestions)

    assert result == 'A surprising plot twist!'


def test_generate_plot_twist_missing_fields():
    with pytest.raises(ValueError):
        generate_plot_twist('', 'Introduce a new villain.')

    with pytest.raises(ValueError):
        generate_plot_twist('The hero is on a quest.', '')
