import pytest
from flask import Flask
from src.backend_codebase.views import views_bp
from unittest.mock import patch
from datetime import datetime

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(views_bp)
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@patch('src.backend_codebase.views.generate_chapter_content')
def test_generate_chapter(mock_generate_chapter_content, client):
    mock_generate_chapter_content.return_value = 'Generated content for Test Title based on previous content and user prompts.'

    response = client.post('/generate/chapter', json={
        'title': 'Test Title',
        'previous_content': 'Previous content',
        'user_prompts': 'User prompts'
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Title'
    assert data['content'] == 'Generated content for Test Title based on previous content and user prompts.'
    assert 'chapter_id' in data
    assert 'created_at' in data
    assert datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
