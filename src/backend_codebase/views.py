from flask import Blueprint, request, jsonify
from .services import generate_chapter_content
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
