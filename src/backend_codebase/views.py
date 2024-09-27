from flask import Blueprint, request, jsonify
from .services import generate_chapter_content, generate_character_profile, generate_plot_twist as generate_plot_twist_service
from datetime import datetime, timedelta
import uuid
from .models import User
from .schemas import UserSchema
from sqlalchemy.exc import IntegrityError
from . import db
import bcrypt
import jwt
from .validation import validate_username, validate_email_address, validate_password

views_bp = Blueprint('views', __name__)

# Signup Endpoint
@views_bp.route('/users', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    # Validate inputs
    if not validate_username(username):
        return jsonify({'error': 'Invalid username'}), 400

    if not validate_email_address(email):
        return jsonify({'error': 'Invalid email address'}), 400

    if not validate_password(password):
        return jsonify({'error': 'Invalid password'}), 400

    # Check if the email is already registered
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    # Check if the username is already taken
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create a new user
    new_user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Login Endpoint
@views_bp.route('/sessions', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    # Validate inputs
    if not validate_email_address(email):
        return jsonify({'error': 'Invalid email address'}), 400

    if not password:
        return jsonify({'error': 'Password is required'}), 400

    # Find the user
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Check the password
    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Generate JWT token (replace 'your_secret_key' with your actual secret key)
    token = jwt.encode({'user_id': str(user.id)}, 'your_secret_key', algorithm='HS256')

    return jsonify({'token': token}), 200
