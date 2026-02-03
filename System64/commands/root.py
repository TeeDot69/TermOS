import getpass
import shlex
import importlib
from System64 import auth


def run(args, env):
    if not args:
        print('root: usage root <command> [args...]')
        return
    
    # Ask for root password
    pw = getpass.getpass('[root] password: ')
    
    # Find a root user and verify password
    ok = False
    users_data = auth.load_users()
    for name, user_info in users_data.get('users', {}).items():
        if user_info.get('is_root'):
            if user_info['password'] == auth.hash_password(pw):
                ok = True
                break
    
    if not ok:
        print('root: authentication failed')
        return
    
    # Execute command with root privileges
    cmd = args[0]
    cmd_args = args[1:]
    
    # Create a root environment
    root_env = dict(env)
    root_env['is_root'] = True
    
    # Try to run the command
    try:
        mod = importlib.import_module('System64.commands.' + cmd)
        result = mod.run(cmd_args, root_env)
        return result
    except ModuleNotFoundError:
        print(f'root: command not found: {cmd}')
    except Exception as e:
        print(f'root: error running command: {e}')
