import openai
import os
from dotenv import load_dotenv
import bcrypt
import jwt
from datetime import datetime, timedelta

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
JWT_SECRET = os.getenv('JWT_SECRET', 'your_jwt_secret')
JWT_ALGORITHM = 'HS256'


def generate_chapter_content(title, previous_content, user_prompts):
    """
    Generate the next chapter content based on the title, previous content, and user prompts.

    Parameters:
    title (str): The title of the chapter.
    previous_content (str): The content of the previous chapter.
    user_prompts (str): User-provided prompts for the next chapter.

    Returns:
    str: The generated content for the next chapter.

    Raises:
    ValueError: If any of the input parameters are empty.
    RuntimeError: If the content generation fails.
    """
    if not title or not previous_content or not user_prompts:
        raise ValueError('All input parameters must be provided and non-empty.')

    prompt = f"Title: {title}\nPrevious Content: {previous_content}\nUser Prompts: {user_prompts}\nGenerate the next chapter content:"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate content: {str(e)}")


def generate_character_profile(character_name, traits, backstory):
    """
    Generate a detailed character profile based on the character name, traits, and backstory.

    Parameters:
    character_name (str): The name of the character.
    traits (str): The traits of the character.
    backstory (str): The backstory of the character.

    Returns:
    str: The generated character profile.

    Raises:
    ValueError: If any of the input parameters are empty.
    RuntimeError: If the profile generation fails.
    """
    if not character_name or not traits or not backstory:
        raise ValueError('All input parameters must be provided and non-empty.')

    prompt = f"Character Name: {character_name}\nTraits: {traits}\nBackstory: {backstory}\nGenerate a detailed character profile:"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate character profile: {str(e)}")


def generate_plot_twist(current_plot, user_suggestions):
    """
    Generate a plot twist based on the current plot and user suggestions.

    Parameters:
    current_plot (str): The current plot of the story.
    user_suggestions (str): User-provided suggestions for the plot twist.

    Returns:
    str: The generated plot twist.

    Raises:
    ValueError: If any of the input parameters are empty.
    RuntimeError: If the plot twist generation fails.
    """
    if not current_plot or not user_suggestions:
        raise ValueError('All input parameters must be provided and non-empty.')

    prompt = f"Current Plot: {current_plot}\nUser Suggestions: {user_suggestions}\nGenerate a plot twist:"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate plot twist: {str(e)}")


def hash_password(password):
    """
    Hash a password using bcrypt.

    Parameters:
    password (str): The password to hash.

    Returns:
    str: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def signup(username, password):
    """
    Signup a new user by storing their username and hashed password.

    Parameters:
    username (str): The username of the new user.
    password (str): The password of the new user.

    Returns:
    dict: A dictionary containing the username and hashed password.
    """
    hashed_password = hash_password(password)
    # Here you would typically store the username and hashed_password in the database
    return {'username': username, 'hashed_password': hashed_password}


def generate_token(username):
    """
    Generate a JWT token for a given username.

    Parameters:
    username (str): The username for which to generate the token.

    Returns:
    str: The generated JWT token.
    """
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def login(username, password):
    """
    Authenticate a user and return a JWT token if successful.

    Parameters:
    username (str): The username of the user.
    password (str): The password of the user.

    Returns:
    dict: A dictionary containing the username and JWT token if authentication is successful.

    Raises:
    ValueError: If authentication fails.
    """
    # Here you would typically retrieve the hashed password from the database
    stored_hashed_password = hash_password(password)  # This is just a placeholder

    if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
        token = generate_token(username)
        return {'username': username, 'token': token}
    else:
        raise ValueError('Invalid username or password')
