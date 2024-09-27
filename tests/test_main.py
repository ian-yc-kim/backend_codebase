import pytest
import base64
import os
from backend_codebase.models import Base, UserInput
from backend_codebase.main import app, engine

@pytest.fixture(scope='module')
def test_client():
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'  # Use in-memory SQLite database for testing
    app.config['TESTING'] = True

    # Create the tables in the same database used by the app
    with app.app_context():
        Base.metadata.create_all(engine)

    with app.test_client() as client:
        yield client

    # Optional: Drop the tables after tests
    with app.app_context():
        Base.metadata.drop_all(engine)

@pytest.fixture(scope='module')
def auth_headers():
    credentials = base64.b64encode(b'admin:password123').decode('utf-8')
    return {
        'Authorization': f'Basic {credentials}'
    }

# ... (rest of your test functions)

def test_collect_user_inputs(test_client, auth_headers):
    response = test_client.post('/api/v1/user-inputs', json={
        'plot': 'A hero saves the world',
        'setting': 'Futuristic city',
        'theme': 'Courage and sacrifice',
        'conflict': 'Hero vs villain'
    }, headers=auth_headers)

    assert response.status_code == 201
    assert b'User inputs successfully recorded.' in response.data

    # Optionally, verify the data in the database
    with test_client.application.app_context():
        session = test_client.application.Session()
        user_inputs = session.query(UserInput).all()
        assert len(user_inputs) == 1
        session.close()
