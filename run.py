import openai
import os

CONTEXT_FILE = 'context.txt'
PARAMETERS = {
    'model': 'text-davinci-002',
    'temperature': 0,
}

openai.api_key = os.getenv('OPENAI_API_KEY')

with open(CONTEXT_FILE, 'r') as f:
    text = f.read()

response = openai.Completion.create(prompt=text, **PARAMETERS)
text = response['choices'][0]['text']

with open(CONTEXT_FILE, 'a') as f:
    f.write(text)
