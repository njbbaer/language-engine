import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')


class Prompt:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    # Uses GPT-3 to peforms a completion on the prompt text
    def complete(self, params={}):
        params = {
            'model': 'text-davinci-002',
            'prompt': self.text,
            'temperature': 0,
            **params,
        }
        return openai.Completion.create(**params)['choices'][0]['text']

    # Performs a completion and appends the result to the prompt
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


class ChatEngine():
    def __init__(self, input_name, output_name, header, params={}):
        self.prompt = ChatPrompt(header)
        self.input_name = input_name
        self.output_name = output_name
        self.params = params

    def run_cli(self):
        while True:
            self.prompt.append_newline()
            print(self.input_name, end=': ')
            self.prompt.append_message(self.input_name, input())
            self.prompt.append_message(self.output_name)
            print(self.output_name, end=': ')
            response = self.prompt.complete_message(self.params)
            print(response)


class ShellEngine():
    def __init__(self, username, hostname, header, params=[{}, {}]):
        self.prompt = ShellPrompt(header)
        self.username = username
        self.hostname = hostname
        self.params = [
            {
                'model': 'text-curie-001',
                'stop': '$',
                'max_tokens': 64,
                **params[0],
            },
            {
                'stop': f'{username}@{hostname}',
                'max_tokens': 256,
                **params[1],
            }
        ]

    def run_cli(self):
        self.prompt.append(f'\n{self.username}@{self.hostname}:~$ pwd')
        self.prompt.append(f'\n/home/{self.username}')
        while True:
            self.prompt.append_terminal_prompt(self.username, self.hostname)
            self.prompt.complete_path(self.params[0])
            print(self.prompt.last_line(), end='')
            self.prompt.append(input())
            output = self.prompt.complete_command({
                **self.params[1],
                'stop': f'{self.username}@{self.hostname}'
            })
            print(output, end='')
            if output:
                print()


if __name__ == '__main__':
    ShellEngine(
        username='admin',
        hostname='ubuntu-desktop',
        header=(
            # 'All commands are run with no errors\n'
            'Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-121-generic x86_64)'
        ),
    ).run_cli()
