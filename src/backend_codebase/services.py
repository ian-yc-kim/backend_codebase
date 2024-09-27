import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


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
