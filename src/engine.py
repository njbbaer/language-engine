import requests

from src.completion import Completion


class Engine:
    def __init__(self, context, log, model_params):
        self.model_params = model_params
        self.context = context
        self.log = log

    def run(self):
        with requests.Session() as session:
            self.session = session
            while True:
                self.context.load()
                completion = self._perform_completion()

                self.context.append(completion.output_text)
                self.context.save()

                self.log.record(completion)
                input('Press enter to request completion...')

    def _perform_completion(self):
        prompt = self.context.text
        completion = Completion(prompt, self.model_params)
        print('Making request with ~{} tokens...'.format(completion.num_prompt_tokens()))
        completion.perform(self.session)
        print('Received ~{} tokens.'.format(completion.num_output_tokens()))
        return completion
