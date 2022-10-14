import os
import requests

API_KEY = os.getenv('OPENAI_API_KEY')


def complete(model_params, log=None):
    response = requests.post(
        'https://api.openai.com/v1/completions',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json=model_params,
    )
    completion = response.json()['choices'][0]['text']
    log.record(model_params, completion)
    return completion
