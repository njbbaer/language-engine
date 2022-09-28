import yaml


class Config:
    def __init__(self, filepath):
        self.filepath = filepath
        self.load()

    def load(self):
        with open(self.filepath, 'r') as f:
            self.params = yaml.safe_load(f)

    def get_model_params(self):
        return self.params['model_params']
