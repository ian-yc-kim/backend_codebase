import openai
import os

openai.api_key = os.environ.get('OPENAI_API_KEY')

def generate_content(prompt):
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()
