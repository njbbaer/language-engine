import os
import requests


class Engine:
    def __init__(self, context, log, model_params):
        self.model_params = model_params
        self.context = context
        self.log = log

    def run(self):
        with requests.Session() as session:
            while True:
                self.context.load()
                prompt = self.context.text
                completion = self._complete_prompt(session)

                self.context.append(completion)
                self.context.save()

                self.log.record(prompt, completion, self.model_params)
                input('Press enter to request completion...')

    def _complete_prompt(self, session):
        prompt = self.context.text
        num_tokens = count_tokens(prompt)
        print(f'Making request with ~{num_tokens} tokens...')
        api_key = os.getenv('OPENAI_API_KEY')
        response = session.post(
            'https://api.openai.com/v1/completions',
            headers={'Authorization': f'Bearer {api_key}'},
            json={'prompt': prompt, **self.model_params},
        )
        output_text = response.json()['choices'][0]['text']
        num_tokens = count_tokens(output_text)
        print(f'Received ~{num_tokens} tokens.')
        return output_text


def count_tokens(text):
    return round(len(text) / 4)
