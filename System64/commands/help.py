import pkgutil
import importlib

def run(args, env):
    print('Available commands:')
    # We can list the commands in the package
    import System64.commands as cmds
    for _, name, _ in pkgutil.iter_modules(cmds.__path__):
        print('-', name)
