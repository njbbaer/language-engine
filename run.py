from src.engine import Engine
from src.context import Context
from src.log import Log
from src.config import Config

if __name__ == '__main__':
    Engine(
        context=Context('context.txt'),
        log=Log('log.yml'),
        config=Config('config.yml')
    ).run()
