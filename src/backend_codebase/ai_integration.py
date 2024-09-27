import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

class OpenAIError(Exception):
    pass

class OpenAI:
    def __init__(self, api_key):
        self.api_key = api_key

    def chat_completions_create(self, model, messages, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty
            )
            return response.choices[0].message['content'].strip()
        except openai.error.OpenAIError as e:
            raise OpenAIError(f"An error occurred: {e}")

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_content(prompt):
    return openai_client.chat_completions_create(
        model='gpt-4',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.7,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )