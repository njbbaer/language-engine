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

    def _load(self):
        self.context.load()
        self.config.load()

    def _build_parameters(self, prompt):
        return {
            **self.config.parameters(),
            'prompt': prompt
        }


class BasicEngine(Engine):
    def run(self):
        while True:
            self._load()
            parameters = self._build_parameters(self.context.text)
            print('Making request with ~{} tokens...'.format(count_tokens(parameters['prompt'])))
            completion = complete(parameters, self.log)
            print('Received ~{} tokens.'.format(count_tokens(completion)))
            self.context.append(completion)
            self.context.save()
            input('Press enter to request completion...')


class ChatEngine(Engine):
    def run(self):
        while True:
            input_text = input(f'{self.config["human_name"]}: ')
            self._load()
            prompt = self._build_prompt(input_text)
            parameters = self._build_parameters(prompt)
            completion = complete(parameters, self.log).strip()
            print(f'{self.config["bot_name"]}: {completion}')
            self.context.text = f'{prompt} {completion}'
            self.context.save()

    def _build_prompt(self, input_text):
        return (
            f'{self.context.text}\n'
            f'{self.config["human_name"]}: {input_text}\n'
            f'{self.config["bot_name"]}:'
        )
