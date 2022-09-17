import openai
import os
from ruamel.yaml.scalarstring import LiteralScalarString

from yaml_config import yaml

openai.api_key = os.getenv('OPENAI_API_KEY')


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

    def record(self, prompt, completion, params):
        self.log.append({
            'id': int(self.log[-1]['id']) + 1 if self.log else 0,
            'params': params,
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


class Engine:
    def __init__(self, context_file, log_file, params):
        self.params = params
        self.context = Context(context_file)
        self.log = Log(log_file)

    def run(self):
        while True:
            prompt = self.context.text
            completion = complete_prompt(prompt, self.params)

            self.context.append(completion)
            self.context.save()

            self.log.record(prompt, completion, self.params)
            input()


def complete_prompt(prompt, params):
    response = openai.Completion.create(prompt=prompt, **params)
    return response['choices'][0]['text'].strip()


if __name__ == '__main__':
    Engine('context.txt', 'log.yml', {
        'model': 'text-davinci-002',
        'temperature': 0.0,
    }).run()
