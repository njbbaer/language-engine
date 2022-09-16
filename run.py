import openai
import os
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

openai.api_key = os.getenv('OPENAI_API_KEY')

yaml = YAML()


class Context:
    def __init__(self, filepath):
        self.filepath = filepath
        self.load()

    def append(self, text):
        self.text += text

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                self.text = f.read()
        else:
            self.text = ''

    def save(self):
        with open(self.filepath, 'w') as f:
            f.write(self.text)


class Log:
    def __init__(self, filepath):
        self.filepath = filepath
        self.load()

    def record(self, prompt, completion, parameters):
        self.log.append({
            'id': int(self.log[-1]['id']) + 1 if self.log else 0,
            'parameters': parameters,
            'prompt': LiteralScalarString(prompt) or None,
            'completion': LiteralScalarString(completion) or None,
        })
        self.save()

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                self.log = yaml.load(file.read())
        else:
            self.log = []

    def save(self):
        with open(self.filepath, 'w') as file:
            yaml.dump(self.log, file)


if __name__ == '__main__':
    CONTEXT_FILE = 'context.txt'
    LOG_FILE = 'log.yml'
    PARAMETERS = {
        'model': 'text-davinci-002',
        'temperature': 0.0,
    }

    context = Context(CONTEXT_FILE)
    log = Log(LOG_FILE)

    prompt = context.text
    response = openai.Completion.create(prompt=prompt, **PARAMETERS)
    completion = response['choices'][0]['text'].strip()

    context.append(completion)
    context.save()

    log.record(prompt, completion, PARAMETERS)
