from src.completion import Completion
from src.context import Context
from src.log import Log
from src.config import Config


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
            completion = self._perform_completion()
            self.context.append(completion.output_text)
            input('Press enter to request completion...')

    def _perform_completion(self):
        prompt = self.context.text
        completion = Completion(prompt, self.config, self.log)
        print('Making request with ~{} tokens...'.format(completion.count_prompt_tokens()))
        completion.perform()
        print('Received ~{} tokens.'.format(completion.count_output_tokens()))
        return completion
