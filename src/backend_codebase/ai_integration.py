import openai
import os
import time

openai.api_key = os.getenv('OPENAI_API_KEY')

class OpenAIError(Exception):
    pass

class OpenAI:
    """
    A class to interact with OpenAI's API for generating chat completions.

    Attributes:
    api_key (str): The API key for authenticating with OpenAI.
    """
    def __init__(self, api_key):
        """
        Initializes the OpenAI client with the provided API key.

        Args:
        api_key (str): The API key for authenticating with OpenAI.
        """
        self.api_key = api_key

    def chat_completions_create(self, model, messages, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, retries=3, delay=5):
        """
        Creates a chat completion using the OpenAI API.

        Args:
        model (str): The model to use for generating the completion.
        messages (list): A list of messages to send to the model.
        temperature (float): Sampling temperature.
        max_tokens (int): Maximum number of tokens to generate.
        top_p (float): Nucleus sampling probability.
        frequency_penalty (float): Frequency penalty.
        presence_penalty (float): Presence penalty.
        retries (int, optional): Number of retries in case of failure. Defaults to 3.
        delay (int, optional): Delay between retries in seconds. Defaults to 5.

        Returns:
        str: The generated completion text.

        Raises:
        OpenAIError: If an error occurs after the specified number of retries.
        """
        for attempt in range(retries):
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
                return response['choices'][0]['message']['content'].strip()
            except openai.error.OpenAIError as e:
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    raise OpenAIError(f"An error occurred: {e}")

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_content(prompt):
    """
    Generates content based on the given prompt using OpenAI's GPT-4 model.

    Args:
    prompt (str): The prompt to generate content from.

    Returns:
    str: The generated content.
    """
    return openai_client.chat_completions_create(
        model='gpt-4',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.7,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

class AIIntegration:
    """
    A class to manage the integration with the AI model for generating new content based on the current state and user feedback.

    Attributes:
    current_state (str): The current state of the content.
    user_feedback (str): The feedback provided by the user.
    """
    def __init__(self):
        """
        Initializes the AIIntegration class with default values for current state and user feedback.
        """
        self.current_state = ""
        self.user_feedback = ""

    def update_state(self, new_state):
        """
        Updates the current state with the provided new state.

        Args:
        new_state (str): The new state to update.
        """
        self.current_state = new_state

    def update_feedback(self, feedback):
        """
        Updates the user feedback with the provided feedback.

        Args:
        feedback (str): The feedback to update.
        """
        self.user_feedback = feedback

    def generate_new_content(self):
        """
        Generates new content based on the current state and user feedback.

        Returns:
        str: The generated content.
        """
        prompt = f"Current state: {self.current_state}\nUser feedback: {self.user_feedback}\nGenerate new content:"
        return generate_content(prompt)
