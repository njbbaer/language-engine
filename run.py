import openai
import os
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

CONTEXT_FILE = 'context.txt'
LOG_FILE = 'log.yml'
PARAMETERS = {
    'model': 'text-davinci-002',
    'temperature': 0.0,
}

openai.api_key = os.getenv('OPENAI_API_KEY')

yaml = YAML()

with open(CONTEXT_FILE, 'r') as file:
    prompt = file.read()

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r') as file:
        log = yaml.load(file.read())
else:
    log = []

response = openai.Completion.create(prompt=prompt, **PARAMETERS)
completion = response['choices'][0]['text']

log.append({
    'id': int(log[0]['id']) + 1 if log else 0,
    'parameters': PARAMETERS,
    'prompt': LiteralScalarString(prompt),
    'completion': LiteralScalarString(completion),
})

with open(CONTEXT_FILE, 'a') as file:
    file.write(completion)

with open(LOG_FILE, 'w') as file:
    yaml.dump(log, file)
