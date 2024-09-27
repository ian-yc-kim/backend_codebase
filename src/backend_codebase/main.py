from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, UserInput
from .ai_integration import generate_content
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

@app.route('/generate-content', methods=['POST'])
def generate_content_endpoint():
    user_input = request.json.get('input')
    content = generate_content(user_input)
    return jsonify({'content': content})

if __name__ == '__main__':
    app.run(debug=True)
