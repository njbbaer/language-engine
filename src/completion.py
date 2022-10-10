import os
import requests

API_KEY = os.getenv('OPENAI_API_KEY')


class Completion:
    def __init__(self, prompt_text, config, log):
        self.prompt_text = prompt_text
        self.config = config
        self.log = log

    def perform(self):
        response = requests.post(
            'https://api.openai.com/v1/completions',
            headers={'Authorization': f'Bearer {API_KEY}'},
            json={'prompt': self.prompt_text, **self.config.model_params()},
        )
        self.output_text = response.json()['choices'][0]['text']
        self.log.record(self)

    def count_prompt_tokens(self):
        return count_tokens(self.prompt_text)

    def count_output_tokens(self):
        return count_tokens(self.output_text)


def count_tokens(text):
    return round(len(text) / 4)
