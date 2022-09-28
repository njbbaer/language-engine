from src.completion import Completion


class Engine:
    def __init__(self, context, log, config):
        self.context = context
        self.log = log
        self.config = config

    def run(self):
        while True:
            self.context.load()
            self.config.load()

            completion = self._perform_completion()

            self.context.append(completion.output_text)
            self.context.save()

            self.log.record(completion)
            input('Press enter to request completion...')

    def _perform_completion(self):
        prompt = self.context.text
        completion = Completion(prompt, self.config)
        print('Making request with ~{} tokens...'.format(completion.count_prompt_tokens()))
        completion.perform()
        print('Received ~{} tokens.'.format(completion.count_output_tokens()))
        return completion
