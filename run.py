from src.engine import ChatEngine

if __name__ == '__main__':
    ChatEngine(
        context_file='context.txt',
        config_file='config.yml',
        log_file='log.yml',
    ).run()
