from src.complete import complete
from src.context import Context
from src.log import Log
from src.config import Config
from src.utils import count_tokens


class Engine:
    def __init__(self, context_file, config_file, log_file):
        self.context = Context(context_file)
        self.config = Config(config_file)
        self.log = Log(log_file)

    def _load_files(self):
        self.context.load_file()
        self.config.load_file()


class BasicEngine(Engine):
    def run(self):
        while True:
            self._load_files()
            parameters = {**self.config.parameters(), 'prompt': self.context.text}
            print('Making request with ~{} tokens...'.format(count_tokens(parameters['prompt'])))
            completion = complete(parameters, self.log)
            print('Received ~{} tokens.'.format(count_tokens(completion)))
            self.context.append(completion)
            input('Press enter to request completion...')
