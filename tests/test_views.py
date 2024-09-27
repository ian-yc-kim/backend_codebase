import pytest
from flask import Flask
from src.backend_codebase.views import views_bp
from unittest.mock import patch

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(views_bp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_generate_character(client):
    with patch('src.backend_codebase.views.generate_character_profile') as mock_generate:
        mock_generate.return_value = 'This is a mocked character profile.'
        response = client.post('/generate/character', json={
            'character_name': 'John Doe',
            'traits': 'Brave, Smart',
            'backstory': 'A hero from a small village'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert 'character_id' in data
        assert data['name'] == 'John Doe'
        assert data['profile'] == 'This is a mocked character profile.'
        assert 'created_at' in data


def test_generate_character_missing_fields(client):
    response = client.post('/generate/character', json={
        'character_name': 'John Doe',
        'traits': 'Brave, Smart'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
