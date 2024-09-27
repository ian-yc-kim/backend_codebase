import pytest
from backend_codebase import create_app, db
from backend_codebase.models import User
from backend_codebase.views import views_bp
import bcrypt

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash=bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt())
        )
        db.session.add(user)
        db.session.commit()
        yield db
        db.session.remove()


def test_login_user_success(client, init_database):
    response = client.post('/sessions', json={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data


def test_signup_user_validation(client):
    # Test invalid username
    response = client.post('/users', json={'username': 'ab', 'email': 'valid@example.com', 'password': 'Validpass1'})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Invalid username'

    # Test invalid email
    response = client.post('/users', json={'username': 'validuser', 'email': 'invalidemail', 'password': 'Validpass1'})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Invalid email address'

    # Test invalid password
    response = client.post('/users', json={'username': 'validuser', 'email': 'valid@example.com', 'password': 'short'})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Invalid password'


def test_login_user_validation(client):
    # Test invalid email
    response = client.post('/sessions', json={'email': 'invalidemail', 'password': 'Validpass1'})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Invalid email address'

    # Test invalid password
    response = client.post('/sessions', json={'email': 'test@example.com', 'password': 'wrongpass'})
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Invalid credentials'
