import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


def generate_chapter_content(title, previous_content, user_prompts):
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
