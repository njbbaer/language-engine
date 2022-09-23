from src.engine import Engine
from src.context import Context
from src.log import Log

if __name__ == '__main__':
    Engine(
        context=Context('context.txt'),
        log=Log('log.yml'),
        model_params={
            'model': 'text-davinci-002',
            'temperature': 0.7,
            'max_tokens': 512,
        }
    ).run()
