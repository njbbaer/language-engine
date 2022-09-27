import os
import requests

API_KEY = os.getenv('OPENAI_API_KEY')


class Completion:
    def __init__(self, prompt_text, model_params):
        self.prompt_text = prompt_text
        self.model_params = model_params

    def perform(self):
        response = requests.post(
            'https://api.openai.com/v1/completions',
            headers={'Authorization': f'Bearer {API_KEY}'},
            json={'prompt': self.prompt_text, **self.model_params},
        )
        self.output_text = response.json()['choices'][0]['text']

    def num_prompt_tokens(self):
        return count_tokens(self.prompt_text)

    def num_output_tokens(self):
        return count_tokens(self.output_text)


def count_tokens(text):
    return round(len(text) / 4)
