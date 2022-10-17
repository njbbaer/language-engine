import sys
import io
import unittest
import responses
from unittest.mock import patch

from src.engine import ShellEngine


def mock_openai_completion(request_body, response_text):
    request_body = {
        'model': 'text-davinci-002',
        'temperature': 0,
        **request_body,
    }
    responses.add(
        responses.POST,
        "https://api.openai.com/v1/completions",
        json={
            'choices': [
                {
                    'text': response_text,
                }
            ]
        },
        status=200,
        match=[responses.matchers.json_params_matcher(request_body)],
    )


class TestEngine(unittest.TestCase):

    def assert_stdout(self, mock_stdout, expected_value):
        self.assertEqual(mock_stdout.getvalue(), expected_value)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', lambda *args: 'pwd')
    @responses.activate
    def test_shell_engine(self, mock_stdout):
        mock_openai_completion({
            'model': 'text-curie-001',
            'prompt': (
                'Welcome to Ubuntu\n'
                'admin@ubuntu-desktop:~$ pwd\n'
                '/home/admin\n'
                'admin@ubuntu-desktop:'
            ),
            'stop': '$',
            'max_tokens': 64,
        }, response_text='~')
        mock_openai_completion({
            'model': 'text-davinci-002',
            'prompt': (
                'Welcome to Ubuntu\n'
                'admin@ubuntu-desktop:~$ pwd\n'
                '/home/admin\n'
                'admin@ubuntu-desktop:~$ pwd'
            ),
            'stop': 'admin@ubuntu-desktop',
            'max_tokens': 256,
        }, response_text='/home/admin')
        ShellEngine(
            username='admin',
            hostname='ubuntu-desktop',
            header=(
                'Welcome to Ubuntu'
            ),
        ).run()
        self.assert_stdout(mock_stdout, 'admin@ubuntu-desktop:~$ /home/admin\n')
