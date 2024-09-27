import pytest
from flask import Flask, request, jsonify
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.backend_codebase.models import Base, UserInput
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

@app.route('/api/v1/user-inputs', methods=['POST'])
def collect_user_inputs():
    data = request.get_json()
    required_fields = ['plot', 'setting', 'theme', 'conflict']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    session = Session()
    user_input = UserInput(
        user_id=data.get('user_id'),
        plot=data['plot'],
        setting=data['setting'],
        theme=data['theme'],
        conflict=data['conflict'],
        additional_preferences=data.get('additional_preferences')
    )
    session.add(user_input)
    session.commit()
    session.refresh(user_input)
    session.close()

    return jsonify({'message': 'User inputs successfully recorded.', 'input_id': user_input.id}), 201

if __name__ == '__main__':
    app.run(debug=True)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_collect_user_inputs(client):
    response = client.post('/api/v1/user-inputs', json={
        'plot': 'A thrilling adventure',
        'setting': 'A distant planet',
        'theme': 'Survival',
        'conflict': 'Man vs Nature'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User inputs successfully recorded.'
    assert 'input_id' in response.json

def test_collect_user_inputs_missing_field(client):
    response = client.post('/api/v1/user-inputs', json={
        'plot': 'A thrilling adventure',
        'setting': 'A distant planet',
        'theme': 'Survival'
    })
    assert response.status_code == 400
    assert 'error' in response.json
