import os


class Context:
    def __init__(self, filepath):
        self.filepath = filepath
        self.load()

    def append(self, text, save=True):
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
