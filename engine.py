from prompt import ChatPrompt, ShellPrompt


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