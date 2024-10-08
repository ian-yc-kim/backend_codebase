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
    """
    Collect user inputs from the request and store them in the database.

    This function expects a JSON payload in the request body that conforms to the UserInputSchema.
    It validates the JSON data, stores it in the database, and returns a success message with the input ID.

    Returns:
        Response: A JSON response containing a success message and the input ID, or an error message if validation fails.
    """
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
    """
    Submit feedback from the user and store it in the database.

    This function expects a JSON payload in the request body that conforms to the FeedbackSchema.
    It validates the JSON data, stores it in the database, and returns a success message.

    Returns:
        Response: A JSON response containing a success message, or an error message if validation fails.
    """
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
    """
    Generate content based on user input.

    This function expects a JSON payload in the request body with an 'input' field containing the user's input text.
    It uses the `generate_content` function to generate new content based on the input text and returns the generated content.

    Returns:
        Response: A JSON response containing the generated content, or an error message if the input is missing.
    """
    json_data = request.get_json()
    input_text = json_data.get('input')
    if not input_text:
        return jsonify({'error': 'Input is required.'}), 400
    content = generate_content(input_text)
    return jsonify({'content': content}), 200

@app.route('/api/v1/latest-iteration', methods=['GET'])
@auth.login_required
def get_latest_iteration():
    """
    Retrieve the latest iteration of the novel.

    This function queries the database for the most recent iteration of the novel and returns its content.

    Returns:
        Response: A JSON response containing the latest iteration's content, or an error message if no iterations are found.
    """
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
    """
    Generate a new iteration of the novel based on user input and the current state.

    This function expects a JSON payload in the request body with an 'input' field containing the user's input text.
    It retrieves the latest iteration of the novel from the database, appends the user input to the current state, and generates new content using the `generate_content` function.
    The new content is then stored as a new iteration in the database.

    Args:
        json_data (dict): The JSON payload from the request containing the user's input text.

    Returns:
        Response: A JSON response containing a success message and the new iteration ID, or an error message if the input is missing or content generation fails.
    """
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

    def main():
        """
        The main entry point of the application.

        This function initializes and runs the Flask application.

        Returns:
            None
        """
        app.run(debug=True)
