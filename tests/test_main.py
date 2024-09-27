import pytest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch
from backend_codebase.models import Base, UserInput
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope='module')
def app() -> Flask:
    from backend_codebase.main import app
    return app

@pytest.fixture(scope='module')
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@pytest.fixture(scope='module')
def init_db():
    from backend_codebase.main import engine
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_collect_user_inputs(client: FlaskClient, init_db):
    response = client.post('/api/v1/user-inputs', json={
        'plot': 'A hero saves the day',
        'setting': 'A futuristic city',
        'theme': 'Courage and bravery',
        'conflict': 'An impending disaster'
    })
    assert response.status_code == 201
    assert 'input_id' in response.json
    assert response.json['message'] == 'User inputs successfully recorded.'

    response = client.post('/api/v1/user-inputs', json={
        'setting': 'A futuristic city',
        'theme': 'Courage and bravery',
        'conflict': 'An impending disaster'
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'Missing required field: plot'


def test_generate_content_endpoint(client: FlaskClient):
    mock_response = {
        'choices': [{
            'text': 'Generated content'
        }]
    }

    with patch('backend_codebase.ai_integration.openai.Completion.create', return_value=mock_response):
        response = client.post('/generate-content', json={'input': 'Once upon a time'})
        assert response.status_code == 200
        assert 'content' in response.json
        assert response.json['content'] == 'Generated content'
