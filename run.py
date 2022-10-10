from src.engine import BasicEngine

if __name__ == '__main__':
    BasicEngine(
        context_file='context.txt',
        config_file='config.yml',
        log_file='log.yml',
    ).run()
