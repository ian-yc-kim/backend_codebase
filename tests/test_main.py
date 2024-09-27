import pytest
from unittest.mock import patch
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend_codebase.main import app, collect_user_inputs, submit_feedback, generate_content_endpoint, get_latest_iteration, iterate_novel
from backend_codebase.models import Base, UserInput, NovelIteration
from backend_codebase.schemas import UserInputSchema, FeedbackSchema
import os

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            Base.metadata.create_all(engine)
        yield client
        with app.app_context():
            Base.metadata.drop_all(engine)


def test_collect_user_inputs(test_client: FlaskClient):
    response = test_client.post('/api/v1/user-inputs', json={
        'plot': 'A hero saves the world',
        'setting': 'Futuristic city',
        'theme': 'Courage',
        'conflict': 'Hero vs Villain'
    }, headers={'Authorization': 'Basic YWRtaW46cGFzc3dvcmQxMjM='})
    assert response.status_code == 201
    assert response.json['message'] == 'User inputs successfully recorded.'


def test_submit_feedback(test_client: FlaskClient):
    response = test_client.post('/api/v1/feedback', json={
        'feedback': 'Great story!'
    }, headers={'Authorization': 'Basic YWRtaW46cGFzc3dvcmQxMjM='})
    assert response.status_code == 201
    assert response.json['message'] == 'Feedback successfully recorded.'


def test_generate_content_endpoint(test_client: FlaskClient):
    with patch('backend_codebase.main.generate_content') as mock_generate_content:
        mock_generate_content.return_value = 'Generated content based on the input.'
        response = test_client.post('/api/v1/generate-content', json={
            'input': 'Once upon a time'
        }, headers={'Authorization': 'Basic YWRtaW46cGFzc3dvcmQxMjM='})
        assert response.status_code == 200
        assert 'content' in response.json
        assert response.json['content'] == 'Generated content based on the input.'


def test_get_latest_iteration(test_client: FlaskClient):
    response = test_client.get('/api/v1/latest-iteration', headers={'Authorization': 'Basic YWRtaW46cGFzc3dvcmQxMjM='})
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert 'iteration' in response.json
    else:
        assert response.json['message'] == 'No iterations found.'


def test_iterate_novel(test_client: FlaskClient):
    with patch('backend_codebase.main.generate_content') as mock_generate_content:
        mock_generate_content.return_value = 'New iteration content based on the input.'
        response = test_client.post('/api/v1/iterate-novel', json={
            'input': 'The hero faces a new challenge'
        }, headers={'Authorization': 'Basic YWRtaW46cGFzc3dvcmQxMjM='})
        assert response.status_code == 201
        assert response.json['message'] == 'New iteration generated successfully.'
