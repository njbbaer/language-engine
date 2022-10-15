import yaml


class Config:
    def __init__(self, filepath):
        self.filepath = filepath
        self.load()

    def load(self):
        with open(self.filepath, 'r') as f:
            self.params = yaml.safe_load(f)

    def __getitem__(self, key):
        return self.params[key]

    def __setitem__(self, key, value):
        self.params[key] = value

    def parameters(self):
        included_keys = [
            'model',
            'prompt',
            'max_tokens',
            'temperature',
            'top_p',
            'frequency_penalty',
            'presence_penalty',
            'stop'
        ]
        return dict([
            (i, self.params[i]) for i in self.params if i in set(included_keys)
        ])
