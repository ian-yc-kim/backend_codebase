from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, UserInput
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
    if username in users and check_password_hash(users.get(username), password):
        return username

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

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
    # Here you would retrieve the latest novel iteration from the database
    # For now, we will just return a placeholder message
    return jsonify({'message': 'Latest iteration retrieved successfully.', 'iteration': 'Placeholder for latest iteration'}), 200

if __name__ == '__main__':
    app.run(debug=True)
