import os
from datetime import datetime

from ruamel.yaml.scalarstring import LiteralScalarString
from src.yaml_config import yaml


class Log:
    def __init__(self, filepath):
        self.filepath = filepath
        self._load()

    def record(self, completion):
        self.log.append({
            'id': int(self.log[-1]['id']) + 1 if self.log else 0,
            'timestamp': datetime.now(),
            'params': completion.model_params,
            'prompt': LiteralScalarString(completion.prompt_text) or None,
            'completion': LiteralScalarString(completion.output_text) or None,
        })
        self._save()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                self.log = yaml.load(file.read())
        else:
            self.log = []

    def _save(self):
        with open(self.filepath, 'w') as file:
            yaml.dump(self.log, file)
