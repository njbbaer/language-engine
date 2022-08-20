import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')


class Prompt:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def complete(self, params={}):
        params = {
            'model': 'text-davinci-002',
            'prompt': self.text,
            'temperature': 0,
            **params,
        }
        return openai.Completion.create(**params)['choices'][0]['text']

    def append_completion(self, params={}, strip=False, prefix='', suffix=''):
        output = self.complete(params)
        if strip:
            output = output.strip()
        self.append(prefix + output + suffix)
        return output

    def append(self, text):
        self.text += text

    def append_newline(self):
        self.text += '\n'

    def last_line(self):
        return self.text.split('\n')[-1]


class ChatPrompt(Prompt):
    def append_message(self, name, message=''):
        self.text += f'\n{name}: {message}\n'.rstrip()

    def complete_message(self, params={}):
        return self.append_completion(params, strip=True, prefix=' ')


class ShellPrompt(Prompt):
    def append_terminal_prompt(self, user, host):
        self.text += f'\n{user}@{host}:\n'.rstrip()

    def complete_path(self, params={}):
        return self.append_completion(params, strip=True, suffix='$ ')

    def complete_command(self, params={}):
        return self.append_completion(params, strip=True)
