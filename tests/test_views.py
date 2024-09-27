import pytest
from flask import Flask
from src.backend_codebase.views import views_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(views_bp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_generate_plot_twist(client, mocker):
    mock_generate_plot_twist = mocker.patch('src.backend_codebase.views.generate_plot_twist_service')
    mock_generate_plot_twist.return_value = 'A surprising plot twist!'

    response = client.post('/generate/plot-twist', json={
        'current_plot': 'The hero is on a quest.',
        'user_suggestions': 'Introduce a new villain.'
    })

    assert response.status_code == 201
    data = response.get_json()
    assert 'plot_twist_id' in data
    assert data['content'] == 'A surprising plot twist!'
    assert 'created_at' in data


def test_generate_plot_twist_missing_fields(client):
    response = client.post('/generate/plot-twist', json={
        'current_plot': 'The hero is on a quest.'
    })

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
