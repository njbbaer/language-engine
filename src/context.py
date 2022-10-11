import os


class Context:
    def __init__(self, filepath):
        self.filepath = filepath
        self.reload_file()

    def append(self, text, save=True):
        self.text += text
        if save:
            self.save_file()

    def reload_file(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                self.text = f.read()
        else:
            self.text = ''

    def save_file(self):
        with open(self.filepath, 'w') as f:
            f.write(self.text)
