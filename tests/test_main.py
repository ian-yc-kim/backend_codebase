import pytest
from flask.testing import FlaskClient
from src.backend_codebase.main import app
from base64 import b64encode

@pytest.fixture
def client() -> FlaskClient:
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def get_auth_headers(username, password):
    credentials = f"{username}:{password}"
    token = b64encode(credentials.encode()).decode('utf-8')
    return {
        'Authorization': f'Basic {token}',
    }


def test_collect_user_inputs(client: FlaskClient):
    headers = get_auth_headers('admin', 'password123')
    response = client.post('/api/v1/user-inputs', json={
        'plot': 'A hero saves the world',
        'setting': 'Futuristic city',
        'theme': 'Courage',
        'conflict': 'Hero vs Villain'
    }, headers=headers)
    assert response.status_code == 201
    assert 'input_id' in response.json


def test_generate_content_endpoint(client: FlaskClient, mocker):
    headers = get_auth_headers('admin', 'password123')
    mock_generate_content = mocker.patch('src.backend_codebase.main.generate_content')
    mock_generate_content.return_value = 'Mocked content'
    response = client.post('/api/v1/generate-content', json={
        'input': 'A hero saves the world'
    }, headers=headers)
    assert response.status_code == 200
    assert response.json['content'] == 'Mocked content'


def test_submit_feedback(client: FlaskClient):
    headers = get_auth_headers('admin', 'password123')
    response = client.post('/api/v1/feedback', json={
        'input_id': 12345,
        'feedback': 'Great story!'
    }, headers=headers)
    assert response.status_code == 201
    assert response.json['message'] == 'Feedback successfully recorded.'


def test_get_latest_iteration(client: FlaskClient):
    headers = get_auth_headers('admin', 'password123')
    response = client.get('/api/v1/latest-iteration', headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == 'Latest iteration retrieved successfully.'
    assert 'iteration' in response.json
