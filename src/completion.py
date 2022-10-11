import os
import requests

API_KEY = os.getenv('OPENAI_API_KEY')


def complete(config, log=None):
    response = requests.post(
        'https://api.openai.com/v1/completions',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json=config.model_params(),
    )
    completion = response.json()['choices'][0]['text']
    log.record(config, completion)
    return completion
