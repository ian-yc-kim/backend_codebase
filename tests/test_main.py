import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend_codebase.models import Base, UserInput
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture(scope='module')
def app() -> Flask:
    from backend_codebase.main import app
    return app

@pytest.fixture(scope='module')
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@pytest.fixture(scope='module')
def init_db():
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
