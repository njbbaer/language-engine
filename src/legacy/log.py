import os
from datetime import datetime

from ruamel.yaml.scalarstring import LiteralScalarString
from src.yaml_setup import yaml


class Log:
    def __init__(self, filepath):
        self.filepath = filepath
        self._load()

    def record(self, parameters, completion):
        self._load()
        self.log.append({
            'id': self._get_next_id(),
            'timestamp': datetime.now(),
            'parameters': self._format_parameters(parameters),
            'completion': self._format_string(completion),
        })
        self._save()

    def _format_string(self, text):
        return LiteralScalarString(text.strip()) or None

    def _get_next_id(self):
        return int(self.log[-1]['id']) + 1 if self.log else 0

    def _format_parameters(self, parameters):
        parameters = parameters.copy()
        parameters['prompt'] = self._format_string(parameters['prompt'])
        return parameters

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                self.log = yaml.load(file.read())
        else:
            self.log = []

    def _save(self):
        with open(self.filepath, 'w') as file:
            yaml.dump(self.log, file)
