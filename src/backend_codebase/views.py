from flask import Blueprint, request, jsonify
from .services import generate_chapter_content, generate_character_profile, generate_plot_twist as generate_plot_twist_service
from datetime import datetime
import uuid

views_bp = Blueprint('views', __name__)

@views_bp.route('/generate/chapter', methods=['POST'])
def generate_chapter():
    json_data = request.get_json()
    title = json_data.get('title')
    previous_content = json_data.get('previous_content')
    user_prompts = json_data.get('user_prompts')

    if not title or not previous_content or not user_prompts:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        content = generate_chapter_content(title, previous_content, user_prompts)
        response = {
            'chapter_id': str(uuid.uuid4()),  # Generate a unique chapter ID
            'title': title,
            'content': content,
            'created_at': datetime.utcnow().isoformat() + 'Z'  # Use the current timestamp
        }
        return jsonify(response), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@views_bp.route('/generate/character', methods=['POST'])
def generate_character():
    json_data = request.get_json()
    character_name = json_data.get('character_name')
    traits = json_data.get('traits')
    backstory = json_data.get('backstory')

    if not character_name or not traits or not backstory:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        profile = generate_character_profile(character_name, traits, backstory)
        response = {
            'character_id': str(uuid.uuid4()),  # Generate a unique character ID
            'name': character_name,
            'profile': profile,
            'created_at': datetime.utcnow().isoformat() + 'Z'  # Use the current timestamp
        }
        return jsonify(response), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@views_bp.route('/generate/plot-twist', methods=['POST'])
def generate_plot_twist():
    json_data = request.get_json()
    current_plot = json_data.get('current_plot')
    user_suggestions = json_data.get('user_suggestions')

    if not current_plot or not user_suggestions:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        content = generate_plot_twist_service(current_plot, user_suggestions)
        response = {
            'plot_twist_id': str(uuid.uuid4()),  # Generate a unique plot twist ID
            'content': content,
            'created_at': datetime.utcnow().isoformat() + 'Z'  # Use the current timestamp
        }
        return jsonify(response), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
