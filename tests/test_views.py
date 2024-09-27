import pytest
from flask import Flask
import json
import bcrypt

from backend_codebase.views import views_bp
from backend_codebase.models import User
from backend_codebase import db  # Import the existing db instance

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Initialize the db with the app

    with app.app_context():
        db.create_all()

    app.register_blueprint(views_bp)

    yield app

    # Clean up / reset resources for other tests
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    }


def test_create_user(client, user_data):
    response = client.post('/users', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == user_data['username']
    assert data['email'] == user_data['email']

    # Verify the user is in the database
    with client.application.app_context():
        user = db.session.query(User).filter_by(username=user_data['username']).first()
        assert user is not None
        assert bcrypt.checkpw(user_data['password'].encode('utf-8'), user.password_hash)

    # Test duplicate username
    response = client.post('/users', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == 409
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Username or email already exists'

    # Test duplicate email
    user_data['username'] = 'newuser'
    response = client.post('/users', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == 409
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Username or email already exists'

    # Test missing fields
    response = client.post('/users', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
