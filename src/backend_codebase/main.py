from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, UserInput, NovelIteration
from .ai_integration import generate_content
import os
from dotenv import load_dotenv
from .schemas import UserInputSchema, FeedbackSchema
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
app = Flask(__name__)

# Authentication setup
auth = HTTPBasicAuth()
users = {
    "admin": generate_password_hash("password123")
}

@auth.verify_password
def verify_password(username, password):
    """
    Verify the provided username and password.

    Args:
        username (str): The username to verify.
        password (str): The password to verify.

    Returns:
        str: The username if verification is successful, None otherwise.
    """
    if username in users and check_password_hash(users.get(username), password):
        return username

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
app.Session = Session  # Add Session to app

# Create all tables
with app.app_context():
    Base.metadata.create_all(engine)

@app.route('/api/v1/user-inputs', methods=['POST'])
@auth.login_required
def collect_user_inputs():
    json_data = request.get_json()
    schema = UserInputSchema()
    errors = schema.validate(json_data)
    if errors:
        return jsonify(errors), 400
    data = schema.load(json_data)

    session = Session()
    user_input = UserInput(**data)
    session.add(user_input)
    session.commit()
    session.refresh(user_input)
    session.close()

    return jsonify({'message': 'User inputs successfully recorded.', 'input_id': user_input.id}), 201

# Similarly update other endpoints with validation and authentication

@app.route('/api/v1/feedback', methods=['POST'])
@auth.login_required
def submit_feedback():
    json_data = request.get_json()
    schema = FeedbackSchema()
    errors = schema.validate(json_data)
    if errors:
        return jsonify(errors), 400
    data = schema.load(json_data)

    # Add feedback to the database (implementation depends on your models)

    return jsonify({'message': 'Feedback successfully recorded.'}), 201

@app.route('/api/v1/generate-content', methods=['POST'])
@auth.login_required
def generate_content_endpoint():
    json_data = request.get_json()
    input_text = json_data.get('input')
    if not input_text:
        return jsonify({'error': 'Input is required.'}), 400
    content = generate_content(input_text)
    return jsonify({'content': content}), 200

@app.route('/api/v1/latest-iteration', methods=['GET'])
@auth.login_required
def get_latest_iteration():
    session = Session()
    latest_iteration = session.query(NovelIteration).order_by(NovelIteration.created_at.desc()).first()
    session.close()
    if (latest_iteration):
        return jsonify({'message': 'Latest iteration retrieved successfully.', 'iteration': latest_iteration.content}), 200
    else:
        return jsonify({'message': 'No iterations found.'}), 404

@app.route('/api/v1/iterate-novel', methods=['POST'])
@auth.login_required
def iterate_novel():
    json_data = request.get_json()
    input_text = json_data.get('input')
    if not input_text:
        return jsonify({'error': 'Input is required.'}), 400

    session = Session()
    latest_iteration = session.query(NovelIteration).order_by(NovelIteration.created_at.desc()).first()
    current_state = latest_iteration.content if latest_iteration else ""

    try:
        new_content = generate_content(f"Current state: {current_state}\nUser input: {input_text}")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    new_iteration = NovelIteration(iteration_number=str(int(latest_iteration.iteration_number) + 1 if latest_iteration else 1), content=new_content)
    session.add(new_iteration)
    session.commit()
    session.refresh(new_iteration)
    session.close()

    return jsonify({'message': 'New iteration generated successfully.', 'iteration_id': new_iteration.id}), 201

if __name__ == '__main__':
    app.run(debug=True)
