import os
import sys
import shlex
from System64 import auth
from System64 import ohedit
from System64 import rsrcmntr
from System64 import PATH
import registry


def first_boot_setup():
    print("First boot detected. Let's create accounts.")
    root_user = input('Create root username (default: root): ').strip() or 'root'
    root_pass = input('Create root password: ').strip()
    user_name = input('Create regular username (optional): ').strip()
    user_pass = ''
    if user_name:
        user_pass = input(f'Create password for {user_name}: ').strip()
    auth.create_user(root_user, root_pass, is_root=True)
    if user_name:
        auth.create_user(user_name, user_pass, is_root=False)
    print('First boot setup complete. Please login.')


def login_loop():
    while True:
        if not auth.has_users():
            first_boot_setup()
        username = input('Login username: ').strip()
        password = input('Password: ').strip()
        ok, user = auth.verify_login(username, password)
        if ok:
            return user
        print('Login failed.')


def load_commands():
    # Map command names to module paths under System64.commands
    import importlib
    cmds = {}
    base = 'System64.commands.'
    names = ['ls','rm','mk','wget','zip','unzip','cd','logout','shutdown','date','time','help','echo','battery','cat','clear','root','rsrcmntr','neofetch']
    for n in names:
        try:
            cmds[n] = importlib.import_module(base + n)
        except Exception as e:
            pass
    return cmds


def main():
    commands = load_commands()
    while True:
        user = login_loop()
        # Initialize user home directory
        user_home = PATH.init_user_directories(user['name'])
        env = {'user': user['name'], 'is_root': user.get('is_root', False), 'cwd': user_home, 'home': user_home}
        while True:
            current_dir = env.get('cwd', os.getcwd())
            home_dir = env.get('home', user_home)
            hostname = os.uname().nodename if hasattr(os, 'uname') else 'TermOS'
            
            # Display path in Linux style (no drive letters)
            if current_dir == home_dir:
                display_path = '~'
            else:
                display_path = PATH.linux_path(current_dir)
            
            prompt = f"{env['user']}@{hostname}:{display_path}# " if env['is_root'] else f"{env['user']}@{hostname}:{display_path}$ "
            try:
                line = input(prompt)
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if not line.strip():
                continue
            parts = shlex.split(line)
            cmd = parts[0]
            args = parts[1:]
            if cmd == 'ohedit':
                ohedit.run(args, env)
                continue
            if cmd == 'rsrcmntr':
                rsrcmntr.run(args, env)
                continue
            mod = commands.get(cmd)
            if not mod:
                print('Unknown command:', cmd)
                continue
            try:
                result = mod.run(args, env)
                if result == 'logout':
                    break
                if result == 'shutdown':
                    print('Shutting down TermOS...')
                    sys.exit(0)
            except Exception as e:
                print('Error running command:', e)


if __name__ == '__main__':
    main()
