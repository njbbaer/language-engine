import os
from datetime import datetime

from ruamel.yaml.scalarstring import LiteralScalarString
from src.yaml_config import yaml


class Log:
    def __init__(self, filepath):
        self.filepath = filepath
        self.load()

    def record(self, prompt, completion, params):
        self.log.append({
            'id': int(self.log[-1]['id']) + 1 if self.log else 0,
            'timestamp': datetime.now(),
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
