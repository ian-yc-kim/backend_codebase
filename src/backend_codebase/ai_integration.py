import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_content(prompt):
    response = openai.Completion.create(
        prompt=prompt,
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response['choices'][0]['text'].strip()
