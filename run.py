from src.engine import ShellEngine

ShellEngine(
    username='admin',
    hostname='ubuntu-desktop',
    header=(
        'Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-121-generic x86_64)'
    ),
).run_loop()
